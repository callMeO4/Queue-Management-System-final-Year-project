from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .allocation_service import allocate_customer_to_best_teller
from .models import (
    Customer,
    Queue_Assignment,
    Queue_Ticket,
    Service,
    Teller,
    Wait_Prediction,
)

User = get_user_model()


def _get_or_create_customer(request):
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        return customer

    guest_user, _ = User.objects.get_or_create(
        username='walkin_guest',
        defaults={'role': 'customer', 'first_name': 'Walk-In', 'last_name': 'Customer'},
    )
    customer, _ = Customer.objects.get_or_create(user=guest_user)
    return customer


def service_selection_view(request):
    """Displays available banking services for customers to choose from."""
    services = Service.objects.all().order_by('id')
    return render(request, 'backend/service_selection.html', {'services': services})


def register_queue_ticket(request, service_id):
    """Handles customer queue registration, ticket generation, and dynamic allocation."""
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        customer = _get_or_create_customer(request)

        with transaction.atomic():
            last_ticket = Queue_Ticket.objects.select_for_update().order_by('-id').first()
            next_id = (last_ticket.id + 1) if last_ticket else 1
            ticket_number = f'TCK-{next_id:04d}'

            ticket = Queue_Ticket.objects.create(
                customer=customer,
                service=service,
                ticket_number=ticket_number,
                status='waiting',
            )

        try:
            allocation_result = allocate_customer_to_best_teller(ticket.id)
            return render(
                request,
                'backend/ticket_confirmation.html',
                {'ticket': ticket, 'allocation': allocation_result},
            )
        except ValueError as e:
            ticket.delete()
            return render(
                request, 'backend/error.html', {'error_message': str(e)}
            )

    return redirect('service_selection')


def customer_status_view(request, ticket_number):
    """Allows customers to view their assigned teller, queue position, and estimated wait time."""
    ticket = get_object_or_404(Queue_Ticket, ticket_number=ticket_number)
    assignment = (
        Queue_Assignment.objects.filter(ticket=ticket, is_active=True)
        .select_related('teller', 'teller__user')
        .first()
    )

    queue_position = 0
    if assignment:
        ahead_count = Queue_Assignment.objects.filter(
            teller=assignment.teller,
            is_active=True,
            assigned_at__lt=assignment.assigned_at,
        ).count()
        queue_position = ahead_count + 1

    latest_prediction = (
        Wait_Prediction.objects.filter(ticket=ticket)
        .order_by('-created_at')
        .first()
    )

    return render(
        request,
        'backend/customer_status.html',
        {
            'ticket': ticket,
            'assignment': assignment,
            'queue_position': queue_position,
            'latest_prediction': latest_prediction,
        },
    )


def lobby_display_view(request):
    """Displays active queue tickets and teller counter statuses for the lobby/admin view."""
    active_assignments = (
        Queue_Assignment.objects.filter(is_active=True)
        .select_related('ticket', 'ticket__service', 'teller', 'teller__user')
        .order_by('assigned_at')
    )
    tellers = Teller.objects.select_related('user').order_by('teller_number')
    return render(
        request,
        'backend/lobby_display.html',
        {
            'active_assignments': active_assignments,
            'tellers': tellers,
        },
    )


def update_ticket_status(request, ticket_id, action):
    """Updates a ticket status to serving or completed and closes active assignment on completion."""
    if request.method == 'POST':
        ticket = get_object_or_404(Queue_Ticket, id=ticket_id)
        now = timezone.now()
        if action == 'serving':
            ticket.status = 'serving'
            if not ticket.service_start_time:
                ticket.service_start_time = now
            ticket.save()
        elif action == 'completed':
            ticket.status = 'completed'
            if not ticket.service_start_time:
                ticket.service_start_time = now
            ticket.completion_time = now
            ticket.save()
            Queue_Assignment.objects.filter(ticket=ticket, is_active=True).update(is_active=False)
    return redirect('lobby_display')


def toggle_teller_availability(request, teller_id):
    """Toggles a teller's availability and status state."""
    if request.method == 'POST':
        teller = get_object_or_404(Teller, id=teller_id)
        teller.is_available = not teller.is_available
        teller.current_status_state = 'Ready' if teller.is_available else 'Paused'
        teller.save()
    return redirect('lobby_display')

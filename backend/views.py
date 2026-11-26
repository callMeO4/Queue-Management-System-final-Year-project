from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
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


def _is_counter_staff(user):
    if not user.is_authenticated:
        return False
    role = getattr(user, 'role', None)
    return bool(
        role in {'teller', 'admin'}
        or getattr(user, 'is_staff', False)
        or getattr(user, 'is_superuser', False)
    )


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


def login_view(request):
    """Authenticates users and routes tellers/admins to the lobby display or customers to services."""
    next_url = request.GET.get('next') or request.POST.get('next') or ''
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url, allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)
            if _is_counter_staff(user):
                return redirect('lobby_display')
            return redirect('service_selection')

        error_message = 'Invalid username or password. Please try again.'

    return render(
        request,
        'backend/login.html',
        {'error_message': error_message, 'next_url': next_url},
    )


def logout_view(request):
    """Logs out the current user and returns to service selection."""
    if request.method == 'POST':
        logout(request)
    return redirect('service_selection')


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
    """Allows customers to view their assigned teller, people ahead, queue position, and estimated wait time."""
    ticket = get_object_or_404(Queue_Ticket, ticket_number=ticket_number)
    assignment = (
        Queue_Assignment.objects.filter(ticket=ticket, is_active=True)
        .select_related('teller', 'teller__user')
        .first()
    )

    people_ahead = 0
    queue_position = 0
    if assignment:
        people_ahead = Queue_Assignment.objects.filter(
            teller=assignment.teller,
            is_active=True,
            assigned_at__lt=assignment.assigned_at,
        ).count()
        queue_position = people_ahead + 1

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
            'people_ahead': people_ahead,
            'queue_position': queue_position,
            'latest_prediction': latest_prediction,
        },
    )

def lobby_display_view(request):
    """Displays active queue tickets, per-counter queue counts, and teller counter statuses for tellers/admins."""
    if not request.user.is_authenticated:
        return redirect(f"/login/?next={request.path}")
    if not _is_counter_staff(request.user):
        return render(
            request,
            'backend/error.html',
            {'error_message': 'Only Teller or Admin accounts can access the Counter & Lobby Display.'},
        )

    active_assignments = list(
        Queue_Assignment.objects.filter(is_active=True)
        .select_related('ticket', 'ticket__service', 'teller', 'teller__user')
        .order_by('assigned_at')
    )

    counts_by_teller = {}
    for item in active_assignments:
        counts_by_teller[item.teller_id] = counts_by_teller.get(item.teller_id, 0) + 1

    tellers = list(Teller.objects.select_related('user').order_by('teller_number'))
    for teller in tellers:
        teller.queue_count = counts_by_teller.get(teller.id, 0)

    return render(
        request,
        'backend/lobby_display.html',
        {
            'active_assignments': active_assignments,
            'tellers': tellers,
            'total_queued_count': len(active_assignments),
        },
    )


def view_queues_view(request):
    """Dedicated queue inspection page for tellers and admins across all counters."""
    if not request.user.is_authenticated:
        return redirect(f"/login/?next={request.path}")
    if not _is_counter_staff(request.user):
        return render(
            request,
            'backend/error.html',
            {'error_message': 'Only Teller or Admin accounts can view counter queues.'},
        )

    selected_teller = request.GET.get('teller', '').strip()
    tellers = list(Teller.objects.select_related('user').order_by('teller_number'))

    assignments_qs = (
        Queue_Assignment.objects.filter(is_active=True)
        .select_related('ticket', 'ticket__service', 'teller', 'teller__user')
        .order_by('teller__teller_number', 'assigned_at')
    )
    if selected_teller.isdigit():
        assignments_qs = assignments_qs.filter(teller__teller_number=int(selected_teller))

    all_active = list(
        Queue_Assignment.objects.filter(is_active=True).order_by('teller_id', 'assigned_at')
    )
    position_map = {}
    running_by_teller = {}
    for item in all_active:
        idx = running_by_teller.get(item.teller_id, 0) + 1
        running_by_teller[item.teller_id] = idx
        position_map[item.id] = idx

    latest_preds = {}
    for pred in Wait_Prediction.objects.order_by('-created_at'):
        if pred.ticket_id not in latest_preds:
            latest_preds[pred.ticket_id] = pred.predicted_wait_time

    filtered_assignments = list(assignments_qs)
    for item in filtered_assignments:
        item.queue_position = position_map.get(item.id, 1)
        item.people_ahead = max(0, item.queue_position - 1)
        item.predicted_wait_time = latest_preds.get(item.ticket_id)

    for teller in tellers:
        teller.queue_count = running_by_teller.get(teller.id, 0)

    return render(
        request,
        'backend/view_queues.html',
        {
            'assignments': filtered_assignments,
            'tellers': tellers,
            'selected_teller': selected_teller,
            'total_queued_count': len(all_active),
        },
    )

def update_ticket_status(request, ticket_id, action):
    """Updates a ticket status to serving or completed and syncs teller counter state."""
    if not _is_counter_staff(request.user):
        return redirect(f"/login/?next={request.path}")
    if request.method == 'POST':
        ticket = get_object_or_404(Queue_Ticket, id=ticket_id)
        now = timezone.now()
        active_assignment = (
            Queue_Assignment.objects.filter(ticket=ticket, is_active=True)
            .select_related('teller')
            .first()
        )

        if action == 'serving':
            ticket.status = 'serving'
            if not ticket.service_start_time:
                ticket.service_start_time = now
            ticket.save()
            if active_assignment:
                active_assignment.teller.current_status_state = 'Serving'
                active_assignment.teller.save()
        elif action == 'completed':
            ticket.status = 'completed'
            if not ticket.service_start_time:
                ticket.service_start_time = now
            ticket.completion_time = now
            ticket.save()
            Queue_Assignment.objects.filter(ticket=ticket, is_active=True).update(is_active=False)
            if active_assignment:
                still_serving = Queue_Assignment.objects.filter(
                    teller=active_assignment.teller,
                    is_active=True,
                    ticket__status='serving',
                ).exists()
                active_assignment.teller.current_status_state = (
                    'Serving' if still_serving else 'Ready'
                )
                active_assignment.teller.save()
    return redirect('lobby_display')



def toggle_teller_availability(request, teller_id):
    """Toggles a teller's availability and status state."""
    if not _is_counter_staff(request.user):
        return redirect(f"/login/?next={request.path}")
    if request.method == 'POST':
        teller = get_object_or_404(Teller, id=teller_id)
        teller.is_available = not teller.is_available
        teller.current_status_state = 'Ready' if teller.is_available else 'Paused'
        teller.save()
    return redirect('lobby_display')

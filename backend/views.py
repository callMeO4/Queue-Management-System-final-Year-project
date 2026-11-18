from django.shortcuts import get_object_or_404, redirect, render
from .allocation_service import allocate_customer_to_best_teller
from .models import Customer, Queue_Assignment, Queue_Ticket, Service


def service_selection_view(request):
  """Displays available banking services for customers to choose from."""
  services = Service.objects.all()
  return render(request, 'backend/service_selection.html', {'services': services})


def register_queue_ticket(request, service_id):
  """Handles customer queue registration, ticket generation, and dynamic allocation."""
  if request.method == 'POST':
    service = get_object_or_404(Service, id=service_id)

    # For prototype simplicity, link to the logged-in customer or create a default session customer
    customer, created = Customer.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None
    )

    # Generate a unique ticket number (e.g., TCK-1001)
    last_ticket = Queue_Ticket.objects.all().order_by('-id').first()
    next_id = (last_ticket.id + 1) if last_ticket else 1
    ticket_number = f'TCK-{next_id:04d}'

    # Create the queue ticket
    ticket = Queue_Ticket.objects.create(
        customer=customer, service=service, ticket_number=ticket_number, status='waiting'
    )

    # Trigger dynamic allocation mechanism
    try:
      allocation_result = allocate_customer_to_best_teller(ticket.id)
      return render(
          request,
          'backend/ticket_confirmation.html',
          {'ticket': ticket, 'allocation': allocation_result},
      )
    except ValueError as e:
      return render(
          request, 'backend/error.html', {'error_message': str(e)}
      )

  return redirect('service_selection')


def customer_status_view(request, ticket_number):
  """Allows customers to view their assigned teller, queue position, and estimated wait time."""
  ticket = get_object_or_404(Queue_Ticket, ticket_number=ticket_number)
  assignment = Queue_Assignment.objects.filter(
      ticket=ticket, is_active=True
  ).first()

  # Dynamically calculate queue position (number of active waiting tickets ahead of this one for the same teller)
  queue_position = 1
  if assignment:
    queue_position = (
        Queue_Assignment.objects.filter(
            teller=assignment.teller,
            is_active=True,
            assigned_at__lt=assignment.assigned_at,
        ).count()
        + 1
    )

  return render(
      request,
      'backend/customer_status.html',
      {
          'ticket': ticket,
          'assignment': assignment,
          'queue_position': queue_position,
      },
  )


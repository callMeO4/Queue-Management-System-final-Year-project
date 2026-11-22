from datetime import datetime
from ml_models.ml_models.predictor import QueueWaitTimePredictor
from .models import Queue_Assignment, Queue_Ticket, Teller, Teller_Service


def allocate_customer_to_best_teller(ticket_id: int):
  """Dynamically allocates a queue ticket to the eligible teller with the lowest predicted waiting time."""
  try:
    ticket = Queue_Ticket.objects.get(id=ticket_id)
  except Queue_Ticket.DoesNotExist:
    raise ValueError(f'Queue ticket with ID {ticket_id} does not exist.')

  requested_service = ticket.service

  # 1. Identify tellers who are available and configured to provide the requested service
  eligible_teller_services = Teller_Service.objects.filter(
      service=requested_service, teller__is_available=True
  )

  if not eligible_teller_services.exists():
    raise ValueError(
        'No available tellers found for the requested service category.'
    )

  predictor = QueueWaitTimePredictor()
  # (Optional: In production, load a pre-trained model file via joblib/pickle here)

  best_teller = None
  lowest_wait_time = float('inf')
  current_hour = datetime.now().hour

  # 2. Evaluate predicted waiting time for each eligible teller
  for ts in eligible_teller_services:
    teller = ts.teller

    # Calculate current queue length for this specific teller
    active_queue_length = Queue_Assignment.objects.filter(
        teller=teller, is_active=True
    ).count()

    estimated_duration = requested_service.estimated_service_duration

    # Predict wait time using our Scikit-learn model logic
    predicted_wait = predictor.predict_wait_time(
        queue_length=active_queue_length,
        estimated_duration=estimated_duration,
        hour_of_day=current_hour,
    )

    # 3. Track the teller with the lowest predicted wait time
    if predicted_wait < lowest_wait_time:
      lowest_wait_time = predicted_wait
      best_teller = teller

  if best_teller:
    # Assign the ticket to the best teller
    assignment = Queue_Assignment.objects.create(
        ticket=ticket, teller=best_teller, is_active=True
    )
    ticket.status = 'waiting'
    ticket.save()

    return {
        'status': 'success',
        'assigned_teller': best_teller.teller_number,
        'predicted_wait_time': round(lowest_wait_time, 2),
        'ticket_number': ticket.ticket_number,
    }

  raise ValueError('Failed to allocate teller due to an unexpected error.')


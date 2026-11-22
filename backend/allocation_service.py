from datetime import datetime
from ml_models.ml_models.predictor import QueueWaitTimePredictor
from .models import Queue_Assignment, Queue_Ticket, Teller, Teller_Service, Wait_Prediction


def allocate_customer_to_best_teller(ticket_id: int):
  """Dynamically allocates a queue ticket to the eligible teller with the lowest predicted waiting time."""
  try:
    ticket = Queue_Ticket.objects.get(id=ticket_id)
  except Queue_Ticket.DoesNotExist:
    raise ValueError(f'Queue ticket with ID {ticket_id} does not exist.')

  requested_service = ticket.service

  eligible_teller_services = Teller_Service.objects.filter(
      service=requested_service, teller__is_available=True
  )

  if not eligible_teller_services.exists():
    raise ValueError(
        'No available tellers found for the requested service category.'
    )

  predictor = QueueWaitTimePredictor()

  best_teller = None
  lowest_wait_time = float('inf')
  current_hour = datetime.now().hour

  for ts in eligible_teller_services:
    teller = ts.teller

    active_queue_length = Queue_Assignment.objects.filter(
        teller=teller, is_active=True
    ).count()

    estimated_duration = requested_service.estimated_service_duration

    predicted_wait = predictor.predict_wait_time(
        queue_length=active_queue_length,
        estimated_duration=estimated_duration,
        hour_of_day=current_hour,
    )

    if predicted_wait < lowest_wait_time:
      lowest_wait_time = predicted_wait
      best_teller = teller

  if best_teller:
    Queue_Assignment.objects.create(
        ticket=ticket, teller=best_teller, is_active=True
    )
    rounded_wait = round(float(lowest_wait_time), 2)
    Wait_Prediction.objects.create(
        ticket=ticket,
        teller=best_teller,
        predicted_wait_time=rounded_wait,
    )
    ticket.status = 'waiting'
    ticket.save()

    return {
        'status': 'success',
        'assigned_teller': best_teller.teller_number,
        'predicted_wait_time': rounded_wait,
        'ticket_number': ticket.ticket_number,
    }

  raise ValueError('Failed to allocate teller due to an unexpected error.')

from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_selection_view, name='service_selection'),
    path(
        'register/<int:service_id>/',
        views.register_queue_ticket,
        name='register_ticket',
    ),
    path(
        'status/<str:ticket_number>/',
        views.customer_status_view,
        name='customer_status',
    ),
    path(
        'lobby/',
        views.lobby_display_view,
        name='lobby_display',
    ),
    path(
        'tickets/<int:ticket_id>/<str:action>/',
        views.update_ticket_status,
        name='update_ticket_status',
    ),
    path(
        'tellers/<int:teller_id>/toggle/',
        views.toggle_teller_availability,
        name='toggle_teller_availability',
    ),
]

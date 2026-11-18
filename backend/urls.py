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
]


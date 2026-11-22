from django.db import migrations


def create_initial_services(apps, schema_editor):
  Service = apps.get_model('backend', 'Service')

  initial_services = [
      {
          'name': 'Deposits',
          (
              'description'
          ): 'Deposit cash or cheques into a bank account.',
          'estimated_service_duration': 5,
      },
      {
          'name': 'Withdrawals',
          'description': 'Withdraw cash from a bank account.',
          'estimated_service_duration': 4,
      },
      {
          'name': 'Account enquiries',
          (
              'description'
          ): 'Check account balances, statements, or details.',
          'estimated_service_duration': 6,
      },
      {
          'name': 'Money transfers',
          'description': 'Transfer funds locally or internationally.',
          'estimated_service_duration': 8,
      },
      {
          'name': 'Loan enquiries',
          'description': 'Consultations regarding loan applications and terms.',
          'estimated_service_duration': 15,
      },
  ]

  for service_data in initial_services:
    Service.objects.get_or_create(
        name=service_data['name'], defaults=service_data
    )


class Migration(migrations.Migration):

  dependencies = [
        ('backend', '0001_initial'),
    ]

  operations = [
      migrations.RunPython(create_initial_services),
  ]


from django.db import migrations, models
from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_passengers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('states', models.PositiveSmallIntegerField()),

                (
                    'passenger',
                    models.ForeignKey(
                        on_delete=models.deletion.DO_NOTHING,
                        to='app.Passenger',
                    ),
                ),
                (
                    'journey_driver',
                    models.ForeignKey(
                        on_delete=models.deletion.DO_NOTHING,
                        to='app.JourneyDriver',
                    ),
                ),
                (
                    'seat',
                    models.ForeignKey(
                        on_delete=models.deletion.DO_NOTHING,
                        to='app.Seat',
                    ),
                ),
                
                ('created_at', DateTimeWithoutTZField(auto_now_add=True)),
                ('updated_at', DateTimeWithoutTZField(null=True)),
            ],
        ),
    ]
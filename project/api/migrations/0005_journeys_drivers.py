from django.db import migrations, models
from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_journeys'),
    ]

    operations = [
        migrations.CreateModel(
            name='JourneyDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('datetime_start', DateTimeWithoutTZField()),
                ('states', models.PositiveSmallIntegerField()),

                (
                    'journey_id',
                    models.ForeignKey(
                        on_delete=models.deletion.DO_NOTHING,
                        to='api.Journey',
                    ),
                ),
                (
                    'driver_id',
                    models.ForeignKey(
                        on_delete=models.deletion.DO_NOTHING,
                        to='api.Driver',
                    ),
                ),
                
                ('created_at', DateTimeWithoutTZField(auto_now_add=True)),
                ('updated_at', DateTimeWithoutTZField(null=True)),
            ],
        ),
    ]
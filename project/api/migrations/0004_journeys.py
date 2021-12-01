from django.db import migrations, models
from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_locations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                
                ('duration_in_seconds', models.PositiveBigIntegerField()),
                ('is_active', models.BooleanField(default=True)),

                (
                    'location_id_origin',
                    models.ForeignKey(
                        on_delete=models.deletion.DO_NOTHING,
                        to='api.Location',
                    ),
                ),
                (
                    'location_id_destination',
                    models.ForeignKey(
                        on_delete=models.deletion.DO_NOTHING,
                        to='api.Location',
                    ),
                ),

                ('created_at', DateTimeWithoutTZField(auto_now_add=True)),
                ('updated_at', DateTimeWithoutTZField(null=True)),
            ],
        ),
    ]
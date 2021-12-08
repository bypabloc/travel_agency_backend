from django.db import migrations, models
from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_locations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                
                ('duration_in_seconds', models.PositiveBigIntegerField()),
                ('is_active', models.BooleanField(default=True)),

                (
                    'location_origin',
                    models.ForeignKey(
                        on_delete=models.deletion.DO_NOTHING,
                        to='app.Location',
                    ),
                ),
                (
                    'location_destination',
                    models.ForeignKey(
                        on_delete=models.deletion.DO_NOTHING,
                        to='app.Location',
                    ),
                ),

                ('created_at', DateTimeWithoutTZField(auto_now_add=True)),
                ('updated_at', DateTimeWithoutTZField(null=True)),
            ],
        ),
    ]
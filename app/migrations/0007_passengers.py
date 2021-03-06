from django.db import migrations, models
from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_seats'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                
                ('document', models.CharField(max_length=15, unique=True)),
                ('names', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('date_of_birth', DateTimeWithoutTZField()),
                ('is_whitelist', models.BooleanField(default=True)),

                ('created_at', DateTimeWithoutTZField(auto_now_add=True)),
                ('updated_at', DateTimeWithoutTZField(null=True)),
            ],
        ),
    ]
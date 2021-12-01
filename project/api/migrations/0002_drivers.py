from django.db import migrations, models
from ..helpers.date_time_without_tz_field import DateTimeWithoutTZField

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_buses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                
                ('document', models.CharField(max_length=15, unique=True)),
                ('names', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('date_of_birth', DateTimeWithoutTZField()),
                ('is_active', models.BooleanField(default=True)),

                (
                    'bus',
                    models.ForeignKey(
                        on_delete=models.deletion.DO_NOTHING,
                        to='api.Bus',
                    ),
                ),

                ('created_at', DateTimeWithoutTZField(auto_now_add=True)),
                ('updated_at', DateTimeWithoutTZField(null=True)),
            ],
        ),
    ]

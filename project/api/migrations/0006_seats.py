from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_journeys_drivers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('seat_x', models.PositiveSmallIntegerField()),
                ('seat_y', models.CharField(max_length=1)),
                ('is_active', models.BooleanField(default=True)),
                
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
            ],
        ),
    ]
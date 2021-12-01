from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_drivers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                
                ('name', models.CharField(max_length=50, unique=True)),

                ('is_active', models.BooleanField(default=True)),

                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
            ],
        ),
    ]
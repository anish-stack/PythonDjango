# Generated by Django 4.2.7 on 2024-02-01 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_assignengineer_machine_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignengineer',
            name='travel_by',
            field=models.CharField(max_length=254),
        ),
    ]
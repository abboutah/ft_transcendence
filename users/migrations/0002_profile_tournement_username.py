# Generated by Django 4.2.9 on 2024-03-08 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tournement_username',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

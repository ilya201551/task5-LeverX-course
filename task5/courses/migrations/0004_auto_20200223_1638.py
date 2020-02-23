# Generated by Django 3.0.3 on 2020-02-23 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20200223_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to=settings.AUTH_USER_MODEL),
        ),
    ]

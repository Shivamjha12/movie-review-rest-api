# Generated by Django 3.1.7 on 2021-09-21 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0006_auto_20210917_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='review_by_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

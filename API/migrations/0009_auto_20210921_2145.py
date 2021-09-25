# Generated by Django 3.1.7 on 2021-09-21 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0008_auto_20210921_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='review_by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.1.13 on 2024-05-23 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actions',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='actions',
            index=models.Index(fields=['-created'], name='actions_act_created_639f69_idx'),
        ),
        migrations.AddIndex(
            model_name='actions',
            index=models.Index(fields=['target_ct', 'target_id'], name='actions_act_target__5ecc2e_idx'),
        ),
    ]

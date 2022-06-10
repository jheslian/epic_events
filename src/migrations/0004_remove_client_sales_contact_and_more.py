# Generated by Django 4.0.4 on 2022-06-09 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('src', '0003_event_description_event_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='sales_contact',
        ),
        migrations.RemoveField(
            model_name='event',
            name='support_contact',
        ),
        migrations.CreateModel(
            name='StatusContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.contract')),
                ('sales_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_contact', to=settings.AUTH_USER_MODEL)),
                ('support_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='support_contact', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

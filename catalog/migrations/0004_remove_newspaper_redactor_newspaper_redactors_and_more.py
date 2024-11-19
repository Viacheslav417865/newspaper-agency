# Generated by Django 5.1.3 on 2024-11-18 11:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_newspaper_options_alter_redactor_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newspaper',
            name='redactor',
        ),
        migrations.AddField(
            model_name='newspaper',
            name='redactors',
            field=models.ManyToManyField(related_name='newspaper_redactors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='redactor',
            name='newspapers',
            field=models.ManyToManyField(related_name='redactor_newspapers', to='catalog.newspaper'),
        ),
        migrations.AlterField(
            model_name='newspaper',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newspapers', to='catalog.topic'),
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-13 18:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newspaper',
            options={'ordering': ['-published_date']},
        ),
        migrations.AlterModelOptions(
            name='redactor',
            options={
                'ordering': ['years_of_experience', 'username'],
                'verbose_name': 'redactor',
                'verbose_name_plural': 'redactors'
            },
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['title']},
        ),
        migrations.RemoveField(
            model_name='topic',
            name='name',
        ),
        migrations.AddField(
            model_name='newspaper',
            name='main_img',
            field=models.ImageField(
                default='images/Default.jpg',
                upload_to='images/',
            ),
        ),
        migrations.AddField(
            model_name='topic',
            name='title',
            field=models.CharField(
                default='Default Title',
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name='newspaper',
            name='published_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='newspaper',
            name='redactor',
            field=models.ManyToManyField(
                related_name='newspapers',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='newspaper',
            name='title',
            field=models.CharField(
                max_length=255,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name='newspaper',
            name='topic',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='newspapers',
                to='catalog.topic',
            ),
        ),
        migrations.AlterField(
            model_name='redactor',
            name='years_of_experience',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='ActivateToken',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID',
                )),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(
                    blank=True,
                    default=None,
                    max_length=64,
                    unique=True,
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tokens',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name_plural': 'Activation tokens',
            },
        ),
    ]

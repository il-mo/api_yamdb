# Generated by Django 2.2.16 on 2021-10-09 11:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reviews', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='reviews',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='reviews',
                to='reviews.Title',
            ),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to='reviews.Review',
            ),
        ),
    ]

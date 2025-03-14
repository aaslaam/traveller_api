# Generated by Django 5.1.6 on 2025-03-14 04:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Comments',
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name_plural': 'comments'},
        ),
        migrations.AlterModelTable(
            name='comments',
            table='places_comments',
        ),
    ]

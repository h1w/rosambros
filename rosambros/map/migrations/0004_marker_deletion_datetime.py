# Generated by Django 4.0.6 on 2022-08-03 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_alter_marker_deletion_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='deletion_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

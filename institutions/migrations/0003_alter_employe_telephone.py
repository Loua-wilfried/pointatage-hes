# Generated by Django 5.2.3 on 2025-07-03 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_employe_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='telephone',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

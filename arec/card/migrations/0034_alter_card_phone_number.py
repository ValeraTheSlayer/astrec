# Generated by Django 4.1.6 on 2023-02-10 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0033_card_last_approval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='phone_number',
            field=models.BigIntegerField(),
        ),
    ]

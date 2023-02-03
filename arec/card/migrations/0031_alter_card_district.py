# Generated by Django 4.1.5 on 2023-02-03 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0030_card_received_at_alter_card_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='district',
            field=models.CharField(choices=[('almaty', 'Алматы'), ('baikonur', 'Байконур'), ('esil', 'Есиль'), ('nura', 'Нура'), ('saryarka', 'Сарыарка')], max_length=12),
        ),
    ]

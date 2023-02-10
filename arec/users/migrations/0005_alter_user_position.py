# Generated by Django 4.1.6 on 2023-02-09 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_merge_20230209_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(choices=[('OPERATOR', 'Оператор'), ('LEAD_ENGINEER', 'Ведущий инженер'), ('HEAD_SERVICE', 'Начальник службы'), ('HEAD_SCPE', 'Начальник СКПЭ'), ('CONTROLLER', 'Контроллер')], max_length=30),
        ),
    ]

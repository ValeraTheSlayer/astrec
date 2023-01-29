# Generated by Django 4.1.5 on 2023-01-27 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0005_cardindividual_cardlegalentity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='OBJECT_CATEGORY',
            new_name='object_category',
        ),
        migrations.AlterField(
            model_name='card',
            name='individual_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='individuals', to='card.cardindividual'),
        ),
        migrations.AlterField(
            model_name='card',
            name='legal_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='legal_entities', to='card.cardlegalentity', unique=True),
        ),
    ]

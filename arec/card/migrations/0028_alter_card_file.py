# Generated by Django 4.1.5 on 2023-01-30 09:22

import django.core.files.storage
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0027_alter_card_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='file',
            field=models.FileField(blank=True, storage=django.core.files.storage.FileSystemStorage(location='/code/files'), upload_to='%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]

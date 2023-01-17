from django.db import models


class Card(models.Model):
    """
    Основная таблица заявки абонента
    """
    # ФИО поля
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic_name = models.CharField(max_length=50)

    phone_number = models.PositiveIntegerField()

    district = models.CharField(max_length=125)
    street = models.CharField(max_length=125)
    bldg = models.CharField(max_length=8)  # номер дома, CharField, т.к. включены дроби, буквы и т.п.
    block = models.CharField(max_length=8)
    apt_num = models.CharField(max_length=6)  # номер квартиры, CharField, т.к. тоже бывает с буквами

    floor = models.PositiveIntegerField()
    entrance = models.PositiveSmallIntegerField(default=1)  # номер подъезда
    square = models.DecimalField(decimal_places=2, max_digits=6)  # площадь

    connection_point = models.CharField(max_length=125)
    power = models.CharField(max_length=8)
    nominal = models.PositiveSmallIntegerField()
    main_point = models.CharField(max_length=125)

    counter_number = models.CharField(max_length=25)
    counter_model = models.CharField(max_length=50)

    contract = models.CharField(max_length=50)  # номер и дата договора
    organization = models.CharField(max_length=250)
    operator = models.CharField(max_length=250)  # ФИО оператора TODO: as relation with User model
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO: files
    # TODO: relations to the Approval model

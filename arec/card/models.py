from django.core.files.storage import FileSystemStorage
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models

fs = FileSystemStorage(location='/code/files')
DOC_TYPES = (
    ('realty_contract', 'Договор на помещение'),
    ('tech_passport', 'Технический паспорт'),
    ('identification', 'Удостоверение личности'),
    ('tech_condition', 'Техническое условие'),
    ('dividing_act', 'Акт раздела границы'),
    ('others', 'Другие документы'),
)

TASK = (
    ('Change_of_owner', 'Cмена владельца'),
    ('Primary_registration', 'Первичная регистрация'),
    ('Other', 'Иное'),
)

OBJECT_CATEGORY = (
    ('Garage', 'Гараж'),
    ('House', 'Дом'),
    ('Office', 'Офис'),
    ('Industrial_base', 'Производственная база'),
    ('Other', 'Иное'),
)


class Card(models.Model):
    """
    Основная таблица заявки абонента
    """

    task = models.CharField(max_length=60, null=True,
                            blank=True, choices=TASK)
    object_category = models.CharField(max_length=30, null=True,
                                       blank=True, choices=OBJECT_CATEGORY)

    phone_number = models.PositiveIntegerField()

    city = models.CharField(max_length=125)
    district = models.CharField(max_length=125)
    street = models.CharField(max_length=125)
    bldg = models.CharField(
        max_length=8)  # номер дома, CharField, т.к. включены дроби, буквы и т.п.
    block = models.CharField(max_length=8)
    apt_num = models.CharField(
        max_length=6)  # номер квартиры, CharField, т.к. тоже бывает с буквами

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
    operator = models.CharField(
        max_length=250)  # ФИО оператора TODO: as relation with User model
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    individual_entity = models.OneToOneField('CardIndividual',
                                             on_delete=models.SET_NULL,
                                             null=True,
                                             blank=True,
                                             )
    legal_entity = models.OneToOneField('CardLegalEntity',
                                        on_delete=models.SET_NULL, null=True,
                                        blank=True,
                                        )
    file = models.FileField(
        storage=fs,
        upload_to='%Y/%m/%d/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    # TODO: relations to the Approval model

    class Meta:
        ordering = ['-created_at']


# class DocScan(models.Model):
#     """
#     Прикрепляемые к заявке документы
#     """
#     doctype = models.CharField(max_length=15, choices=DOC_TYPES)
#     doc_file = models.FileField(storage=fs, upload_to='docs/%Y/%m/%d/')
#     upload_at = models.DateTimeField(auto_now_add=True)
#
#     card = models.ForeignKey(Card, on_delete=models.CASCADE)


class CardIndividual(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic_name = models.CharField(max_length=50)
    iin = models.CharField(validators=[RegexValidator(
        r'^\d{12}$', 'Введите корректный ИИН')], max_length=12)


class CardLegalEntity(models.Model):
    company_name = models.CharField(max_length=100)
    bin = models.CharField(validators=[RegexValidator(
        r'^\d{12}$', 'Введите корректный БИН')], max_length=12)

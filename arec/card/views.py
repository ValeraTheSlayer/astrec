import os
import tempfile

from openpyxl.reader.excel import load_workbook
from pikepdf import Pdf
import logging
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from django.db.models import Count, F, Func, Value, CharField

from approval.models import Approval
from arec.settings import AREC_POSITIONS, BASE_DIR

from .models import Card, DOC_TYPES, CardIndividual, CardLegalEntity
from .mappings import xl_map
from .forms import SubscriberCardForm as CardForm, CardIndividualForm, \
    CardLegalEntityForm
from .filters import CardFilter
from .utils import my_view

logger = logging.getLogger(__name__)
entity_map = {'individual': CardIndividual, 'legal': CardLegalEntity}


# rendering main page
@my_view
def main_page(request):
    """
    Главная страница, дашборд и статистика заявок
    """
    # TODO: пока отображает список заявок, в будущем д.б. дашборд
    return render(request, 'html/index.html')


@my_view
def card_list(request, entity='individual'):
    """
    Функция просмотра карточех определенного типа
    """
    cards = Card.objects.select_related(f'{entity}_entity').filter(
        is_archived=False,
        **{f'{entity}_entity__isnull': False})
    ourfilter = CardFilter(request.GET, queryset=cards)
    cards = ourfilter.qs
    return render(request, 'card/card_list.html',
                  {'cards': cards, 'OurFilter': ourfilter, 'entity': entity})


@my_view
def card_archive(request, entity='individual'):
    """
    Функция для создания архива карточек
    """
    cards = Card.objects.filter(is_archived=True)
    ourfilter = CardFilter(request.GET, queryset=cards)

    return render(request, 'card/card_list.html',
                  {'cards': cards, 'is_individual': True,
                   'entity': entity,
                   'OurFilter': ourfilter})


@my_view
def card_approval_registry(request, entity='individual'):
    """
    Функция согласования
    """
    # TODO: only individuals for now, enlarge to legal ones after the next iteration of demo
    if request.method == "POST":
        # TODO: validate and create a bulk of bids
        bids = [int(i) for i in request.POST.getlist('bids[]')]
        cards = Card.objects.filter(id__in=bids)
        approved_list = [
            Approval(
                approving_person=request.user,
                # fix position at the approving_position field to be able to switch user.position
                # keeping the previous position in the approval entity
                approving_position=request.user.position,
                card_ref=card,
                parent=card.last_approval
            )
            for card in cards]
        app_ids = Approval.objects.bulk_create(approved_list)
        messages.add_message(request, messages.SUCCESS,
                             f'Согласованы {len(app_ids)} из {len(cards)} заявок')

        for card, approval in zip(cards, app_ids):
            card.last_approval = approval
        Card.objects.bulk_update(cards, ['last_approval'])

    position_order = [position[0] for position in AREC_POSITIONS]
    approving_position = position_order[position_order.index(request.user.position) - 1]

    filter_kwargs = {'last_approval__approving_position': approving_position}
    #  if approving_position == 'OPERATOR_SCPE':
    #      filter_kwargs['district'] = request.user.district

    cards_to_approve = Card.objects.select_related('last_approval',
                                                   'last_approval__approving_person') \
        .filter(**filter_kwargs).order_by('last_approval__approved_at')

    ourfilter = CardFilter(request.GET, queryset=cards_to_approve)
    filtered_cards_to_approve = ourfilter.qs

    return render(request, 'card/card_registry.html',
                  {'cards': filtered_cards_to_approve, 'OurFilter': ourfilter,
                   'is_individual': entity == 'individual'})


@my_view
def card_detail(request, cid, entity='individual'):
    """
    Функция для создания информации о конкретной карточке
    """
    card = Card.objects.get(pk=cid)
    approvals = Approval.objects.filter(card_ref=cid).values_list('approving_position', flat=True)
    position_titles = {position[0]: position[1].upper() for position in
                       AREC_POSITIONS}
    merge_url = reverse('merge_pdfs', args=[card.id])
    context = {'title': 'Детали карточки',
               'card': card, 'approvals': approvals,
               'position_buttons': position_titles,
               'is_individual': entity == 'individual', 'merge_url': merge_url}
    return render(request, 'card/card_detail.html', context=context)


@my_view
def card_create(request):
    """
    Функция для создания карточки
    """
    if request.method == "POST":
        form = CardForm(request.POST or None)
        link = request.get_full_path()
        is_individual = 'individual' in link
        form_secondary = CardIndividualForm(
            request.POST or None) if is_individual else CardLegalEntityForm(
            request.POST or None)
        # TODO: elaborate how to decrease save() calls for the card_obj
        if form.is_valid() and form_secondary.is_valid():
            with transaction.atomic():
                card_secondary_obj = form_secondary.save()
                card_obj = form.save(commit=False)
                card_obj.received_at = datetime.strptime(
                    request.POST.get('created_date') + ', ' + request.POST.get(
                        'created_time'), '%Y-%m-%d, %H:%M')
                if is_individual:
                    card_obj.individual_entity = card_secondary_obj
                else:
                    card_obj.legal_entity = card_secondary_obj
                card_obj.save()
                approval_obj = Approval(approving_person=request.user,
                                        card_ref=card_obj)
                approval_obj.save()
                card_obj.last_approval = approval_obj
                card_obj.save()
                attachment = request.FILES.get('file')
                if attachment and attachment.name.endswith('.pdf'):
                    card_obj.file = attachment
                    card_obj.save()
                elif attachment:
                    messages.add_message(request, messages.ERROR,
                                         'Загружать можно только файлы формата .PDF')
                messages.add_message(request, messages.SUCCESS,
                                     'Заявка успешно создана!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'При добавлении карточки обнаружены ошибки! Проверьте заполнение.' + str(
                                     form.errors))
    else:
        form = CardForm()
        link = request.get_full_path()
        is_individual = 'individual' in link
        form_secondary = CardIndividualForm(
            request.POST or None) if is_individual else CardLegalEntityForm(
            request.POST or None)

    return render(request, 'card/card_create_form.html', {'form': form,
                                                          f'form_{"individual" if is_individual else "legal_entity"}': form_secondary,
                                                          'is_individual': is_individual})


@my_view
def card_statistics(request):
    """
    Функция для создания статистики
    """
    filters = {}
    for param in ['operator', 'power', 'task', 'object_category',
                  'phone_number', 'city', 'district', 'street', 'bldg',
                  'block', 'apt_num', 'floor', 'entrance', 'square',
                  'connection_point', 'nominal', 'main_point',
                  'counter_number',
                  'counter_model', 'contract', 'organization', 'comment',
                  ]:
        if request.GET.get(param, None):
            filters[f'{param}'] = request.GET.get(param)

    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date and end_date:
        filters['created_at__range'] = [start_date, end_date]
    elif start_date:
        filters['created_at__gte'] = start_date
    elif end_date:
        filters['created_at__lte'] = end_date

    cards = Card.objects.filter(**filters)
    district_counts = cards.values('district').annotate(Count('id'))
    district_stats = {}
    for district in district_counts:
        district_stats[district['district']] = district['id__count']

    return JsonResponse({"card_stats_by_district": district_stats})


@my_view
def merge_pdfs(request, cid):
    """
    Функция для добавления pdf файлов в уже существующий файл.
    В данном проекте функция используется для добавления акта контроллером.
    После добавления акта карточка попадает в архив
    """
    card = Card.objects.get(pk=cid)

    if request.method == 'POST':
        # TODO: validate user.position is CONTROLLER
        if 'pdf_file' not in request.FILES:
            messages.add_message(request, messages.WARNING,
                                 'Пожалуйста, выберите файл для загрузки')
        else:
            pdf_file = request.FILES['pdf_file']
            with Pdf.open(card.file.path,
                          allow_overwriting_input=True) as input_pdf, Pdf.open(
                pdf_file) as new_pdf:
                input_pdf.pages.extend(new_pdf.pages)
                page_number = len(input_pdf.pages) - len(new_pdf.pages) + 1
                card.act_page_number = page_number
                card.is_archived = True
                card.save()
                input_pdf.save(card.file.path)
            messages.add_message(request, messages.SUCCESS,
                                 f'Файл "{pdf_file}" успешно приклеплен на странице {page_number}')

    return redirect('card_detail', cid=cid)


@my_view
def download_selected_cards(request):
    # Получаем список выбранных заявок из POST-запроса
    bids = [int(i) for i in request.POST.getlist('bids[]')]
    # Преобразование объекта Datetime в строчный вид
    formatted_date = Func(
        F('received_at'),
        Value('DD-MM-YYYY'),
        function='to_char',
        output_field=CharField()
    )
    formatted_time = Func(
        F('received_at'),
        Value('HH:MM'),
        function='to_char',
        output_field=CharField()
    )

    # Получаем соответствующие объекты модели Card
    cards = Card.objects.select_related('individual_entity') \
        .annotate(date_as_str=formatted_date, time_as_str=formatted_time) \
        .values(
        'date_as_str',
        'time_as_str',
        'city',
        'district',
        'street',
        'bldg',
        'block',
        'entrance',
        'floor',
        'apt_num',
        'individual_entity__last_name',
        'individual_entity__first_name',
        'individual_entity__patronymic_name',
        'individual_entity__iin',
        'phone_number',
        'object_category',
        'square',
        'connection_point',
        'power',
        'nominal',
        'main_point',
        'counter_model',
        'counter_number',
        'contract',
        'organization'
    ).filter(id__in=bids)

    # Загружаем excel-шаблон и выбираем первый лист
    xl_workbook = load_workbook(
        filename=os.path.join(BASE_DIR, 'registry_template.xlsx'))
    xl_sheet = xl_workbook.worksheets[0]

    # Заполняем ячейки в excel-файле с помощью словаря xl_map
    for row_n, card in enumerate(cards):
        for col, field_name in xl_map.items():
            xl_sheet[f'{col}{row_n + 2}'].value = card[field_name]

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as xl_file:
        xl_workbook.save(xl_file.name)

        with open(xl_file.name, 'rb') as fh:
            response = HttpResponse(fh.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response[
                'Content-Disposition'] = f'attachment; filename={os.path.basename(xl_file.name)}'
            return response

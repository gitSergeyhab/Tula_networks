from datetime import datetime


# def just_titles(request):
#     return {
#         'tit_substations': 'Подстанции',
#         'tit_subscribers': 'Организации',
#         'tit_phones': 'Телефоны',
#         'tit_persons': 'Ответственные лица',
#         'tit_sections': 'Секции',
#         'tit_lines': 'Линии',
#         'tit_feeders': 'Фидеры',
#         'tit_substation': 'Подстанция',
#         'tit_subscriber': 'Организация',
#         'tit_phone': 'Телефон',
#         'tit_person': 'Ответственныо лицо',
#         'tit_section': 'Секция',
#         'tit_line': 'Линия',
#         'tit_feeder': 'Фидер',
#     }


def add_titles(request):
    return {
        'title': 'Тульские Сети',
        'title_add': 'Добавить',
        'title_upd': 'Редактировать',
        'title_del': 'Удалить',
        'title_feeder': 'фидер',
        'title_substation': 'подстанцию',
        'title_subscriber': 'организацию',
        'title_phone': 'телефон',
        'title_person': 'лицо',
        'title_section': 'секцию',
        'title_line': 'линию',
        'title_char': 'характеристики фидера',
    }


def logik(request):
    return {
        'current_year': datetime.now().year,
        'logik_metod': request.path[1:5],
        'logik_obj': request.path[4:10],
        'logik_add': 'add_',
        'logik_upd': 'upd_',
        'logik_del': 'del_',
        'logik_feeder': '_feede',
        'logik_substation': '_subst',
        'logik_subscriber': '_subsc',
        'logik_phone': '_phone',
        'logik_person': '_perso',
        'logik_section': '_secti',
        'logik_line': '_line/',
        'logik_char': '_chara'
    }


def signs(request):
    return {
        'context_menu': {
            'substations': 'Подстанции',
            'lines': 'Линии',
            'sfeeders': 'Фидеры',
            'subscribers': 'Организации',
            'persons': ' Ответственные лица',
            'phones': 'Телефоны',
        }
    }


def class_volt(request):
    return {
        'feeder_6': "btn btn-light border-success px-3 py-0 mx-1",
        'feeder_10': "btn btn-light border-primary px-3 py-0 mx-1",
        'feeder_x': "btn btn-secondary px-3 py-0 mx-1",
        'line_35': "border-danger btn btn-dark py-0 px-4 m-1 vl-border",
        'line_110': 'border-warning btn btn-dark py-0 px-4 m-1 vl-border',
        'line_x': 'btn btn-secondary py-0 px-4 m-1',

    }

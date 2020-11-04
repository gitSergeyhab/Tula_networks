from datetime import datetime


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
    }


def logik(request):
    return {
        'current_year': datetime.now().year,
        'logik_kostyl': '/35',
        'logik_volt2': request.path[-3:-1],
        'logik_volt': request.path[-4:-1],
        'logik_group': request.path[-2:-1],
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
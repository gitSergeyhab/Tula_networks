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
    }


def logik(request):
    return {
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



    }

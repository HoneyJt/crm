
from django.db.models import Q


'''多条件查询 对吧  返回查询的条件'''

def table_filter(request,admin_class):


    print(request.GET.items())
    '''条件过滤'''
    filter_dict = {}
    for k,v in request.GET.items():
        if k == 'page' or k == 'o' or k == '_q':
            print('--------------------')
            continue
        if v:
            filter_dict[k] = v
    return admin_class.model.objects.filter(**filter_dict),filter_dict


def table_sort(request,objs):
    sort_key = request.GET.get('o')
    if sort_key:
        if sort_key.startswith('-'):
            sort_key = sort_key.strip('-')
        else:
            sort_key = '-%s'%sort_key
        return objs.order_by(sort_key),sort_key


    return objs,sort_key


def table_search(request,admin_class,objs):
    search_key = request.GET.get('_q','')
    search_filter = Q()
    search_filter.connector = 'OR'

    for filter in admin_class.search_fields:
        search_filter.children.append(("%s__contains"%filter,search_key))

    res = objs.filter(search_filter)


    print('-----------11111111111111-------------%s'%search_key)

    return res,search_key
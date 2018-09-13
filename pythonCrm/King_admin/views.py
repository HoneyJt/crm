from django.shortcuts import render

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from King_admin.utils import table_filter,table_sort,table_search

from King_admin import king_admin

# Create your views here.


def index(request):
    print(king_admin.enable_admins)
    return render(request,'king_admin/table_index.html',{'table_list':king_admin.enable_admins})

def display_table_objs(request,app_name,table_name):

    admin_class = king_admin.enable_admins[app_name][table_name]
    # 执行分页操作
    # res_list =  admin_class.model.objects.all()

    object_list,filter_conditions = table_filter(request,admin_class)

    object_list,search_key = table_search(request,admin_class,object_list)

    obj_list,sort_key = table_sort(request,object_list)

    print('--------%s'%sort_key)

    paginator = Paginator(obj_list,admin_class.list_per_page)
    print(paginator.num_pages)



    # 取出前端的第几页
    page = request.GET.get('page')

    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # 默认就是第一次 会调用
        query_sets = paginator.page(1)

    except EmptyPage:
        query_sets = paginator.page(paginator.num_pages)

    # 查询结果 和查询条件


    print(query_sets)


    print(admin_class)
    return render(request,'king_admin/table_objs.html',{'admin_class':admin_class,'query_sets':query_sets,'filter_conditions':filter_conditions,'sort_key':sort_key,'search_key':search_key})
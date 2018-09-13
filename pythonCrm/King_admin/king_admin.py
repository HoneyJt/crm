

from crm import models

enable_admins = {}

# 模拟admin的功能
#  自定义admin的功能


class BaseAdmin(object):
    list_display = []
    list_filters = []
    list_per_page = 1


class CustomerAdmin(BaseAdmin):
    list_display = ['qq', 'name', 'source', 'consultant', 'consult_course', 'date', 'status']
    list_filters = ['source', 'consultant', 'consult_course', 'status']
    search_fields = ['qq','name','consultant__name']

class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer', 'consultant', 'date')


def register(model_class,admin_class=None):



    app_name = model_class._meta.app_label

    print(app_name)
    table_name = model_class._meta.model_name

    if app_name not in enable_admins:
        enable_admins[app_name] = {}

    # 给model的数据动态绑定一个admin 这样节省再次获取
    admin_class.model = model_class
    enable_admins[app_name][table_name] = admin_class


register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
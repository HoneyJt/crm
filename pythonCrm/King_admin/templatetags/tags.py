
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag()
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag()

def get_query_sets(admin_class):
    return admin_class.model.objects.all()


@register.simple_tag()
def build_data_row(obj,admin_class):
    ele = ''

    for column in admin_class.list_display:
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:
            column_data = getattr(obj,'get_%s_display' %column)()
        else:
            column_data = getattr(obj,column)
        if type(column_data).__name__ == 'datetime':
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")

        ele += '<td>%s</td>' % column_data
    return mark_safe(ele)



@register.simple_tag()
def render_page(query_sets,filter_conditios,sort_key,search_key):

    filters = ''
    # source = 1 & consultant = 3 & consult_course = 2 & status = 0

    if sort_key:
        if '-' in sort_key:
            sort_key = sort_key.strip('-')



    print('------------------%s%s'%(query_sets,sort_key))
    for k,v in filter_conditios.items():
        filters += '&%s=%s'%(k,v)

    ele = ''
    dot_exit = False
    # 当前页  query_sets.number   需求就是展示最前面的两页 和最后两页  当前页的前后页
    for num in query_sets.paginator.page_range:
        if abs(num - query_sets.number)<=1 or num <3 or num>query_sets.paginator.count-2:
            ele_class = ''

            if num == query_sets.number:
                ele_class = 'active'
            if sort_key:
               ele += '''<li class="%s"><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>'''%(ele_class,num,filters,sort_key,search_key,num)
            else:
                ele += '''<li class="%s"><a href="?page=%s%s&_q=%s">%s</a></li>''' % (ele_class, num, filters,search_key, num)
        else:
            if dot_exit == False:
                ele += '''<li ><a>...</a></li>'''
                dot_exit = True

    return mark_safe(ele)


@register.simple_tag()
def render_filter_ele(condition,admin_class,filter_conditios):

    ele = '''<select class="form-control" name="%s"><option value="">---</option>'''%condition

    filed_obj = admin_class.model._meta.get_field(condition)

    if filed_obj.choices:
        for item in filed_obj.choices:
            selected = ''
            if filter_conditios.get(condition) == str(item[0]):
                selected = 'selected'

            ele+='''<option value="%s" %s>%s</option>'''%(item[0],selected,item[1])

    if type(filed_obj).__name__ ==  'ForeignKey' :

        for ch_item in filed_obj.get_choices()[1:]:
            selected = ''
            if filter_conditios.get(condition) == str(ch_item[0]):
                selected = 'selected'

            ele += '''<option value="%s" %s>%s</option>''' % (ch_item[0],selected,ch_item[1])


    ele+='</select>'


    print(filter_conditios,condition)

    return mark_safe(ele)


@register.simple_tag()
def render_filter_next(filter_conditios,sort_key,search_key):
    filters = ''
    # source = 1 & consultant = 3 & consult_course = 2 & status = 0
    for k, v in filter_conditios.items():
        filters += '&%s=%s' % (k, v)
    if sort_key:
        if '-' in sort_key:
            sort_key = sort_key.strip('-')
        filters+= '&o=%s'%sort_key
    if search_key:
        filters += '&_q=%s'%search_key

    return filters


# 将a标签的内容进行更改  加入排序条件
@register.simple_tag()
def build_filter_btn(column,sort_key,filter_conditions):
    filters = ''
    sort_icon = ''
    # source = 1 & consultant = 3 & consult_course = 2 & status = 0
    for k, v in filter_conditions.items():
        filters += '&%s=%s' % (k, v)

    ele = '''<th><a href="?o={sort_key}{filter_condition}">{column} {sort_icon}</a></th>'''
    if sort_key:
       #  正序
       if column == sort_key.strip('-'):
           if '-' in sort_key:
               sort_icon = '''<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>'''
           else:
    #        倒叙
               sort_icon = '''<span class="glyphicon glyphicon-triangle-top" aria-hidden="true"></span>'''
       else:
            sort_key = column

    else:
        sort_key = column
    print('----------%s-------%s' % (sort_key, column))
    ele = ele.format(sort_key = sort_key,column=column,filter_condition=filters,sort_icon=sort_icon)
    return mark_safe(ele)


from django import template

register = template.Library()

@register.filter
def get_value(dictionary_list, key):
    for item in dictionary_list:
        if item[key]:
            return item[key]
    return None
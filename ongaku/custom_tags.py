from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    """リストを指定された数の要素を持つリストのリストに分割する"""
    return [value[i:i + arg] for i in range(0, len(value), arg)]
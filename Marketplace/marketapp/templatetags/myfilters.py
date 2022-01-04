from django import template

register = template.Library()

def TextSplit(value):
    return value.split(" ")[0]
register.filter("strsplit",TextSplit)
from django import template
from main.models import *

register = template.Library()


@register.simple_tag()
def get_len(array):
    return len(array)

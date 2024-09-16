from django import template
register = template.Library()

@register.simple_tag
def multiple_args_tag(a, b, c):
   return abs(int(a) - int(b)) <= c
    
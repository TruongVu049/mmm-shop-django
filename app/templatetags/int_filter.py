from django import template 
  
register = template.Library() 
  
@register.filter() 
def parseInt(value): 
    return int(value)
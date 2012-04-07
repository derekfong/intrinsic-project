from django import template

register = template.Library()

@register.filter(name='get_key_value')
def get_key_value(dictionary, key_value):
	return dictionary.get(key_value)
	
register.filter('get_key_value', get_key_value)
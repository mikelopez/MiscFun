# custom filters for templates - mike 2009 - 420

from django.template import Library

register = Library()

@register.filter
def firstcharacters(value, arg):
	try:
		v = str(value)
		count = int(arg)
		strs = v[:count]
		strs.replace('<br>','').replace('<BR>','<font', '').replace('<','').replace('<p>','').replace('<P>','')
		return strs
	
	except:
		return value

	


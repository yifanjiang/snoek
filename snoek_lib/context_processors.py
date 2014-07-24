from django.template import RequestContext
import settings

def custom_proc(request):
		return {
				'settings':settings
				}

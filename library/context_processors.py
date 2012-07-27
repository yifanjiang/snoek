from django.template import RequestContext
from snoek import settings

def custom_proc(request):
		return {
				'settings':settings
				}

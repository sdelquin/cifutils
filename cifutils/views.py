from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings


@ensure_csrf_cookie
def index(request):
    return render_to_response('cifutils/base.html', {'DEBUG': settings.DEBUG})

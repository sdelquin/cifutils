from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'pdf/', views.get_pdf),
    url(r'xlsx/', views.get_xlsx),
]

from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', TemplateView.as_view(template_name="main.html"), name='home'),
    path('send-email', views.SendFormEmail.as_view(), name = 'send_email'),
    path('test1', views.e_list, name='home1'),
]

from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name='solo'
urlpatterns = [
    # path('', TemplateView.as_view(template_name='solo/main.html')),
    path('', views.MainView.as_view()),
]


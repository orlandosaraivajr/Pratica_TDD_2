from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('read', views.read, name='read'),
    path('update', views.update, name='update'),
    path('confirm_update', views.confirm_update, name='confirm_update'),
    path('delete', views.delete, name='delete'),
]
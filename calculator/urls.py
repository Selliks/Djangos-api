from django.urls import path
from . import views

urlpatterns = [
    path('calculate/', views.calculate, name='add'),
    path('add_action/', views.add_action, name='add_action'),
    path('delete_action/', views.delete_action, name='delete_action'),
    path('rename_action/', views.rename_action, name='rename_action'),
    path('get_all_action/', views.get_all_action, name='get_all_action'),
]

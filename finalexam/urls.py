from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),    
    path('signup/', views.signup, name='signup'), 
    path('login/', views.login_view, name='login_view'),   
    path('logout/', views.logout_view, name='logout_view'), 
    path('create/', views.create_view, name='create_view'), 
    path('Add/', views.add, name='add'), 
    path('added/', views.add1, name='add1'),
    path('remove/<int:pk>/', views.remove, name='remove'), 
    path('removed/<int:pk>/', views.remove1, name='remove1'),  
    path('edit/<int:pk>/', views.edit, name='edit'),  
    path('edited/<int:pk>/', views.edit1, name='edit1'),      
    path('export/', views.export, name='export'), 
    path('import/', views.import1, name='import1'), 
    path('imports/', views.simple_upload, name='simple_upload'),
]
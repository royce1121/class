from django.urls import path
from . import views
from django.conf.urls import url
from finalexam.views import Home
# from myapp.views import CreateView
# from myapp.views import Signup
# from myapp.views import LoginView
# from myapp.views import LogoutView
# from myapp.views import Add
# from myapp.views import Add1
# from myapp.views import Remove
# from myapp.views import Remove1
# from myapp.views import Edit


urlpatterns = [
    path('', Home.as_view(), name='Home'),
    url(r'signup/$', views.qwerty.as_view(), name='zxcv'),
    url(r'login/$', views.LoginView.as_view(), name='login_view'),
    url(r'logout/$', views.LogoutView.as_view(), name='LogoutView'),
    url(r'Add/$', views.Add.as_view(), name='Add'),
    url(r'remove/(?P<pk>\d+)/$', views.Remove.as_view(), name='remove'),
    url(r'removed/(?P<pk>\d+)/$', views.Remove1.as_view(), name='remove1'),
    url(r'edit/(?P<pk>\d+)/$', views.Edit.as_view(), name='edit'),
    # path('edited/<int:pk>/', views.edit1, name='edit1'),
    url(r'export/', views.export.as_view(), name='export'),
    url(r'import/', views.import1.as_view(), name='import1'),
    # path('imports/', views.simple_upload, name='simple_upload'),
]

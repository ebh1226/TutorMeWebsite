"""mysite URL Configuration
testing something

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))



    '''path('loggingIn', TemplateView.as_view(template_name="home.html")),'''
    
]
"""


from django.contrib import admin
from django.urls import path, include
from tutorme11.views import google_auth
from tutorme11.views import home,index
from tutorme11.views import choose_user_type
from tutorme11.views import loggedInHomePage
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from tutorme11.views import loggedOut 
from tutorme11.views import create_tutorme_user
from tutorme11.views import tutor_dashboard, tutoree_dashboard, view_requests, accept_request, reject_request, user_profile, add_request
from django.urls import path
from tutorme11.views import pay_now

urlpatterns = [
    path("admin/", admin.site.urls),
    path('google-auth/', google_auth, name='google-auth'),
    path('home/', home, name='home'),
    path('accounts/', include('allauth.urls')),
    path('index/',index,name='index'),
    path('', home, name='home'),

    path('choose-user-type/', choose_user_type, name='choose_user_type'),

    path('loggedInHomePage/', loggedInHomePage, name='loggedInHomePage'),

    path('logout', LogoutView.as_view(), name='logout'),

    path('loggedOut/', loggedOut, name='loggedOut'),

    path('loginPage2', create_tutorme_user, name='create_tutorme_user'),
    path('tutor-dashboard/', tutor_dashboard, name='tutor_dashboard'),
    path('tutoree-dashboard/', tutoree_dashboard, name='tutoree_dashboard'),
    
    path('view_requests/', view_requests, name='view_requests'),

    path('<int:request_id>/accept_request/', accept_request, name="accept_request"),
    path('<int:request_id>/reject_request/', reject_request, name="reject_request"),

    path('user/<str:username>/', user_profile, name='user_profile'),
    path('pay_now/<str:tutor_username>/', pay_now, name='pay_now'),

    path('<str:student_username>/<str:tutor_username>/add_request', add_request, name='add_request'),
]

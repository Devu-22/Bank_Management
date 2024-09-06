from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
			path('', views.homepage, name='homepage'),
			path('register/', views.register, name='register'),
			path('login/', views.user_login, name='login'),
			path('logout/', views.user_logout, name='logout'),
			path('dashboard/', views.dashboard, name='dashboard'),
			path('create_account/', views.create_account, name='create_account'),
			path('deposit/', views.deposit, name='deposit'),
			path('withdraw/', views.withdraw, name='withdraw'),
			path('transaction_history/', views.transaction_history, name='transaction_history'),
]
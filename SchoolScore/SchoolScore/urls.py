"""
URL configuration for SchoolScore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
"""
from django.contrib import admin
from django.urls import path
from score import views

urlpatterns = [
    path('', views.index, name='home'),
    path('scores/<int:param>', views.score_table, name='scores'),
    path('create_scores/', views.create_all_score_combinations, name='create_all_scores'),
    path('score/create/', views.ScoreCreateView.as_view(), name='score_create'),
    path('score/<int:pk>/update/<int:param>/', views.ScoreUpdateView.as_view(), name='score_update'),
    path('admin/', admin.site.urls),
]

from django.urls import path
from . import views

#all the urls are defined
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-player/', views.create_player, name='create_player'),
    path('view-players/', views.view_players, name='view_players'),
    path('marketplace/', views.view_marketplace, name='view_marketplace'),
    path('finances/', views.view_finances, name='view_finances'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('view_staff/',views.view_staff,name='view_staff'),
    path('analyst-login/',views.analyst_login,name="analyst_login"),
    path('analyst-dashboard/', views.analyst_dashboard, name='analyst_dashboard'),
    path('manage-stats/', views.manage_stats, name='manage_stats'),  # Manage Stats
    path('manage-injuries/', views.manage_injuries, name='manage_injuries'),  # Manage Injuries
    path('manage-stats/', views.manage_stats, name='manage_stats'),  # Manage Stats
    path('update-stats/<int:player_id>/', views.update_stats, name='update_stats'),
    path('delete_injury/<int:injury_id>/', views.delete_injury, name='delete_injury'),
]

from django.urls import path,include
from . import views

urlpatterns = [
    # Route for the main landing page
    path('', views.landing_page, name='landing_page'),
    
    # Route for the code execution API endpoint
    path('execute/', views.execute_code, name='execute_code'),
    path('ask_ai/', views.ask_ai, name='ask_ai'),
    path("__reload__/", include("django_browser_reload.urls")),
]
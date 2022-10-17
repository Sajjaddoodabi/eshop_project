from django.urls import path
from . import views

urlpatterns = [
    # path('', views.contact_us, name="contact-us")
    path('', views.ContactUsView.as_view(), name="contact_us"),
    path('create_profile/', views.CreateProfileView.as_view(), name="create_profile"),
    path('profiles/', views.ProfilesView.as_view(), name="profiles"),
]

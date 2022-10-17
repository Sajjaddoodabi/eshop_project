from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogOutView.as_view(), name='logout_page'),
    path('activate_account/<email_active_code>', views.ActivateAccountViw.as_view(), name='activate_account'),
    path('forget_pass', views.ForgetPassword.as_view(), name='forget_password_page'),
    path('reset_pass/<active_code>', views.ResetPassword.as_view(), name='reset_password_page'),
]

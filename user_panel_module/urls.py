from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPanelDashboardPage.as_view(), name='user_dashboard_page'),
    path('edit_profile', views.EditUserProfilePage.as_view(), name='edit_user_profile_page'),
    path('change_password', views.ChangePassWordPage.as_view(), name='change_password_page'),
    path('user_basket', views.user_basket, name='user_basket_page'),
    path('my_shoping', views.MyShopping.as_view(), name='user_shopping_page'),
    path('my_shoping_detail/<order_id>', views.my_shopping_detail, name='user_shopping_detail_page'),
    path('remove_order_detail', views.remove_order_detail, name='remove_order_detail_ajax'),
    path('change_order_detail', views.change_order_detail, name='change_order_detail_ajax'),
]

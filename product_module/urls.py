from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name="product_list"),
    path('category/<category>', views.ProductListView.as_view(), name="product_categories"),
    path('brand/<brand>', views.ProductListView.as_view(), name="product_brands"),
    path('<slug:slug>', views.ProductDetailView.as_view(), name="product_detail"),
    path('favorite_product/', views.AddFavoriteProduct.as_view(), name="favorite_product"),
    path('add_product_comment/', views.add_product_comments, name="add_product_comment"),
]

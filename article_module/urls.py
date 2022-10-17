from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticlesListView.as_view(), name="article_page"),
    path('category/<str:category>', views.ArticlesListView.as_view(), name="article_by_category_page"),
    path('<pk>/', views.ArticleDetailView.as_view(), name="article_detail_page"),
    path('add_article_comment', views.add_article_comment, name="add_article_comment")
]

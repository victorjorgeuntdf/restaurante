from django.urls import path
from .views import HomeView, MenuListView, ProductDetailView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("menu/", MenuListView.as_view(), name="menu"),
    path("menu/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]

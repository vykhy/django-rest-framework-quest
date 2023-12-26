from django.urls import path

from .import views

urlpatterns = [
    path("", views.ProductListCreateAPIView.as_view()),
    path('<int:pk>/', views.ProductDetailAPIView.as_view()),
    path("all/", views.ProductListAPIView.as_view())
]
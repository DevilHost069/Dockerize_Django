from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('productwise/<slug:data>/', views.productwise, name="productwise"),
    path('singleproduct/<str:pk>/', views.singleproduct, name="singleproduct"),
    path('publishproducts/', views.publishproducts, name="publishproducts"),
    path('ajax/load-subcategory/', views.load_subcategory, name='ajax_load_subcategory'),
    path('editAds/<str:pk>/',views.editAds,name="editAds"),
    path('deleteAds/<str:pk>/',views.deleteAds,name="deleteAds")
]

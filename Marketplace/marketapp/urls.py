from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('productwise/<slug:data>/', views.productwiseAutomobiles, name="productwise"),
    path('productwisepc/<slug:data>/', views.productwisepc, name="productwisepc"),
    path('productwisemobile/<slug:data>/', views.productwisemobile, name="productwisemobile"),
    path('productwiseApparels/<slug:data>/', views.productwiseApparels, name="productwiseApparels"),
    path('productwiseRealState/<slug:data>/', views.productwiseRealState, name="productwiseRealState"),
    path('singleproduct/<str:pk>/', views.singleproduct, name="singleproduct"),
    path('singleproduct/<str:pk>/likes',views.Addlikes,name="likes"),
    path('singleproduct/<str:pk>/dislikes',views.AddDislikes,name="dislikes"),
    path('publishproducts/', views.publishproducts, name="publishproducts"),
    path('ajax/load-subcategory/', views.load_subcategory, name='ajax_load_subcategory'),
    path('editAds/<str:pk>/',views.editAds,name="editAds"),
    path('deleteAds/<str:pk>/',views.deleteAds,name="deleteAds")
]

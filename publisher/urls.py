from django.urls import path

from publisher import views

app_name = 'publisher'

urlpatterns = [
    path('publisher-list/', views.publisher_list, name='publisher_list'),
    path('publisher-detail/<int:id>/', views.publisher_detail, name='publisher_detail'),
    path('publisher-create/', views.publisher_create, name='publisher_create'),
    path('publisher-safe_delete/<int:id>/', views.publisher_safe_delete, name='publisher_safe_delete'),
    path('publisher-update/<int:id>/', views.publisher_update, name='publisher_update'),
    path('publisher-sale/<int:id>/', views.publisher_sale.as_view(), name='publisher_sale'),


]
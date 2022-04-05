from django.urls import path
from backoffice import views


urlpatterns = [
    # LOGIN
    path('login', views.loginView, name='login'),
    
    # INDEX
    path('', views.indexView, name='index'),

    # CLIENTS
    path('all-clients', views.allClientsView, name='all-clients'),
    path('client-details/<str:pk>/', views.clientDetailView, name='client-details'),
    path('new-client', views.newClientView, name='new-client'),
    
    # PRODUCTS
    path('all-products', views.allProductsView, name='all-products'),
    path('product-details/<str:pk>/', views.productDetailView, name='product-details'),
    path('new-product', views.newProductView, name='new-product'),

    # ORDERS
    path('all-orders', views.allOrdersView, name='all-orders'),
    path('order-details/<str:pk>/', views.orderDetailView, name='order-details'),
    path('new-order', views.newOrderView, name='new-order'),
    path('generate-order-delivery', views.generateOrderDelivery, name='generate-order-delivery'),
    path('order-delivery', views.orderDelivery, name='order-delivery'),
    path('order-done', views.orderDone, name='order-done'),
    path('change-order-status', views.changeOrderStatus, name='change-order-status'),
    path('order-delete', views.orderDelete, name='order-delete'),

    # SALES
    path('all-sales', views.allSalesView, name='all-sales'),

    # COMPRAS
    path('all-spendings', views.allSpendingsView, name='all-spendings'),
    path('new-spending', views.newSpendingView, name='new-spending'),
    path('new-purchase', views.newPurchaseView, name='new-purchase'),

]

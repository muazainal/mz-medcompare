"""
URL configuration for medcompare_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from medicines import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('medicine/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('signup/', views.signup, name='signup'),
    path('submit/', views.submit_medicine, name='submit_medicine'),
    path('create-checkout-session/<int:medicine_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('cart/add/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:medicine_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout-cart/', views.checkout_cart, name='checkout_cart'),
    path('purchase-success/', views.purchase_success, name='purchase_success'),
    path('purchase-cancel/', views.purchase_cancel, name='purchase_cancel'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('buy/<int:medicine_id>/', views.create_purchase_session, name='create_purchase_session'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from medicines import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('medicine/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('signup/', views.signup, name='signup'),
    path('submit/', views.submit_medicine, name='submit_medicine'),
    path('edit/<int:pk>/', views.edit_medicine, name='edit_medicine'),
    path('delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),
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
    path('legal/disclaimer/', views.disclaimer, name='disclaimer'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
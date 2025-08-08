"""
URL configuration for auction_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from auctions import views as auction_views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.conf.urls.i18n import i18n_patterns

def test_view(request):
    return HttpResponse(b"Test view works!", content_type="text/html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('language-switch/', auction_views.custom_language_switcher, name='custom_language_switch'),
    path('language-test/', auction_views.language_test, name='language_test'),
    path('test-language/', auction_views.test_language_url, name='test_language'),
    path('test/', test_view),
    path('', auction_views.home_view, name='home'),
    path('products/', auction_views.product_list, name='products'),
    path('list/', auction_views.list_product_view, name='list_product'),
    path('contact/', auction_views.contact_us, name='contact'),
    path('help/', auction_views.need_help, name='need_help'),
    path('register/', auction_views.register_view, name='register'),
    path('login/', auction_views.login_view, name='login'),
    path('logout/', auction_views.logout_view, name='logout'),
    path('dashboard/', auction_views.vendor_dashboard, name='vendor_dashboard'),
    path('dashboard/buyer/', auction_views.buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/edit/<int:pk>/', auction_views.edit_product, name='edit_product'),
    path('dashboard/delete/<int:pk>/', auction_views.delete_product_dashboard, name='delete_product_dashboard'),
    path('become-vendor/', auction_views.become_vendor, name='become_vendor'),
    path('store-setup/', auction_views.store_setup, name='store_setup'),
    path('products/<int:pk>/', auction_views.product_detail, name='product_detail'),
    path('edit-store/', auction_views.edit_store, name='edit_store'),
    path('dashboard/payments/', auction_views.vendor_payments, name='vendor_payments'),
    path('my-bids/', auction_views.my_bids, name='my_bids'),
    path('terms/', auction_views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy/', auction_views.privacy_policy, name='privacy_policy'),
]

urlpatterns += i18n_patterns(
    path('', auction_views.home_view, name='home'),
    path('products/', auction_views.product_list, name='products'),
    path('list/', auction_views.list_product_view, name='list_product'),
    path('contact/', auction_views.contact_us, name='contact'),
    path('help/', auction_views.need_help, name='need_help'),
    path('register/', auction_views.register_view, name='register'),
    path('login/', auction_views.login_view, name='login'),
    path('logout/', auction_views.logout_view, name='logout'),
    path('dashboard/', auction_views.vendor_dashboard, name='vendor_dashboard'),
    path('dashboard/buyer/', auction_views.buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/edit/<int:pk>/', auction_views.edit_product, name='edit_product'),
    path('dashboard/delete/<int:pk>/', auction_views.delete_product_dashboard, name='delete_product_dashboard'),
    path('become-vendor/', auction_views.become_vendor, name='become_vendor'),
    path('store-setup/', auction_views.store_setup, name='store_setup'),
    path('products/<int:pk>/', auction_views.product_detail, name='product_detail'),
    path('edit-store/', auction_views.edit_store, name='edit_store'),
    path('dashboard/payments/', auction_views.vendor_payments, name='vendor_payments'),
    path('my-bids/', auction_views.my_bids, name='my_bids'),
    path('terms/', auction_views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy/', auction_views.privacy_policy, name='privacy_policy'),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

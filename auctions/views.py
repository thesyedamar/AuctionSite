from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Product, Bid, Payment
from .forms import ProductForm, BidForm, CustomUserCreationForm, StoreSetupForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.utils.translation import gettext as _
from django.utils import translation
from django.http import HttpResponseRedirect
from django.utils import translation
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            from auctions.models import Profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.user_type = form.cleaned_data['user_type']
            profile.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            # If vendor, redirect to store setup
            if profile.user_type == 'vendor':
                return redirect('store_setup')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auctions/register.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'auctions/login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect('login')

def home_view(request):
    # Get products with bids first, then fall back to all active products
    products_with_bids = Product.objects.annotate(num_bids=Count('bids')).filter(num_bids__gt=0).order_by('-num_bids', '-created_at')[:6]
    
    if products_with_bids.exists():
        popular_products = products_with_bids
    else:
        # If no products have bids, show all active products
        popular_products = Product.objects.filter(is_active=True).order_by('-created_at')[:6]
    
    return render(request, 'auctions/home.html', {'popular_products': popular_products})

def products_view(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'auctions/products.html', {'products': products})

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'auctions/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    bid_form = BidForm()
    if request.method == 'POST' and request.user.is_authenticated:
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.product = product
            bid.bidder = request.user
            bid.save()
            messages.success(request, 'Your bid has been placed!')
            return redirect('product_detail', pk=product.pk)
    bids = product.bids.order_by('-bid_time')
    current_bid = bids.first().bid_amount if bids.exists() else product.starting_bid
    seller_profile = getattr(product.seller, 'profile', None)
    return render(request, 'auctions/product_detail.html', {
        'product': product,
        'bid_form': bid_form,
        'bids': bids,
        'current_bid': current_bid,
        'seller_profile': seller_profile,
    })

@login_required
def list_product_view(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.user_type != 'vendor':
        return render(request, 'auctions/error.html', {
            'error_title': 'Access Denied',
            'error_message': 'Only vendors can list products. Please become a vendor first.'
        })
    if not profile.store_name or not profile.store_email:
        messages.info(request, 'Please complete your store setup before listing a product.')
        return redirect('store_setup')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print("DEBUG: POST form valid?", form.is_valid())
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            print(f"DEBUG: Product '{product.title}' created successfully with ID {product.id}")
            messages.success(request, 'Product listed successfully!')
            return redirect('products')
        else:
            print("DEBUG: Form errors:", form.errors)
            print("DEBUG: Form data:", request.POST)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    return render(request, 'auctions/list_product.html', {'form': form})

def ensure_profile(user):
    from auctions.models import Profile
    if user.is_authenticated and not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    return getattr(user, 'profile', None)

@login_required
def store_setup(request):
    profile = ensure_profile(request.user)
    # Only allow vendors to access store setup
    if profile.user_type != 'vendor':
        return render(request, 'auctions/error.html', {
            'error_title': 'Access Denied',
            'error_message': 'Only vendors can set up stores. Please become a vendor first.'
        })
    if request.method == 'POST':
        form = StoreSetupForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store setup complete! Welcome to your vendor dashboard.')
            return redirect('vendor_dashboard')
    else:
        form = StoreSetupForm(instance=profile)
    return render(request, 'auctions/store_setup.html', {'form': form})

@login_required
def become_vendor(request):
    profile = ensure_profile(request.user)
    if profile and profile.user_type != 'vendor':
        profile.user_type = 'vendor'
        profile.save()
    # If store info is missing, redirect to setup
    if not profile.store_name or not profile.store_logo or not profile.store_email:
        messages.info(request, 'Please set up your store to continue as a vendor.')
        return redirect('store_setup')
    messages.success(request, 'You are now a vendor!')
    return redirect('vendor_dashboard')

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'auctions/delete_product_confirm.html', {'product': product})

def contact_view(request):
    return render(request, 'auctions/contact.html')

def is_vendor(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.user_type == 'vendor'

@user_passes_test(is_vendor)
def vendor_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    total_sales = sum(
        bid.bid_amount for product in products for bid in product.bids.all()
    )
    active_bids = sum(product.bids.count() for product in products if product.is_active)
    total_products = products.count()
    sold_products = products.filter(is_active=False, bids__isnull=False).distinct().count()
    running_products = products.filter(is_active=True).count()
    pending_products = products.filter(is_active=False, bids__isnull=True).count()
    return render(request, 'auctions/vendor_dashboard.html', {
        'products': products,
        'total_sales': total_sales,
        'active_bids': active_bids,
        'total_products': total_products,
        'sold_products': sold_products,
        'running_products': running_products,
        'pending_products': pending_products,
        'page_title': _("Vendor Dashboard - Auction Site"),
    })

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('vendor_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'auctions/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product_dashboard(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('vendor_dashboard')
    return render(request, 'auctions/delete_product_confirm.html', {'product': product})

@login_required
def edit_store(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = StoreSetupForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store details updated successfully!')
            return redirect('edit_store')
    else:
        form = StoreSetupForm(instance=profile)
    return render(request, 'auctions/edit_store.html', {'form': form})

@user_passes_test(is_vendor)
def vendor_payments(request):
    payments = Payment.objects.filter(vendor=request.user).order_by('-date')
    return render(request, 'auctions/vendor_payments.html', {'payments': payments})

@login_required
def my_bids(request):
    bids = Bid.objects.filter(bidder=request.user).order_by('-bid_time')
    return render(request, 'auctions/my_bids.html', {'bids': bids})

def terms_and_conditions(request):
    return render(request, 'auctions/terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'auctions/privacy_policy.html')

def contact_us(request):
    return render(request, 'auctions/contact_us.html')

def need_help(request):
    return render(request, 'auctions/need_help.html')

def is_buyer(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.user_type == 'buyer'

@login_required
@user_passes_test(is_buyer)
def buyer_dashboard(request):
    from .models import Bid
    bids = Bid.objects.filter(bidder=request.user).select_related('product').order_by('-bid_time')
    won_bids = [bid for bid in bids if not bid.product.is_active and bid.product.bids.first().bidder == request.user]
    return render(request, 'auctions/buyer_dashboard.html', {
        'bids': bids,
        'won_bids': won_bids,
    })

@csrf_exempt
def custom_language_switcher(request):
    """
    Improved custom language switcher view that ensures proper cookie handling and immediate language activation.
    """
    print("=" * 50)
    print("CUSTOM LANGUAGE SWITCHER VIEW CALLED!")
    print("=" * 50)
    print(f"DEBUG: custom_language_switcher called with method: {request.method}")
    print(f"DEBUG: Available languages: {[lang[0] for lang in settings.LANGUAGES]}")
    print(f"DEBUG: Current LANGUAGE_CODE: {getattr(request, 'LANGUAGE_CODE', 'NOT_SET')}")
    print(f"DEBUG: Session django_language: {request.session.get('django_language', 'NOT_SET')}")
    print(f"DEBUG: Cookie django_language: {request.COOKIES.get('django_language', 'NOT_SET')}")
    
    if request.method == 'POST':
        language = request.POST.get('language')
        next_url = request.POST.get('next', '/')
        print(f"DEBUG: POST data - language={language}, next={next_url}")
        print(f"DEBUG: All POST data: {dict(request.POST)}")

        if language in [lang[0] for lang in settings.LANGUAGES]:
            print(f"DEBUG: Valid language {language}, activating...")
            # Activate the language for the current request
            translation.activate(language)
            # Set the language in the session
            request.session['django_language'] = language
            # Set the language cookie
            import re
            next_url_clean = re.sub(r'^/(en|ar)/', '/', next_url)
            if language != settings.LANGUAGE_CODE:
                next_url_redirect = f'/{language}{next_url_clean}'
            else:
                next_url_redirect = next_url_clean
            response = HttpResponseRedirect(next_url_redirect)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language, max_age=365*24*60*60)
            print(f"DEBUG: Language set to {language}, redirecting to {next_url_redirect}")
            return response
        else:
            print(f"DEBUG: Invalid language {language}")
    else:
        print(f"DEBUG: Not a POST request")
    # If not POST, redirect to home
    response = HttpResponseRedirect('/')
    return response

def test_language_url(request):
    """
    Simple test view to verify URL routing
    """
    print("=" * 50)
    print("TEST LANGUAGE URL VIEW CALLED!")
    print("=" * 50)
    return HttpResponse("Test view works! URL routing is working.")

def language_test(request):
    return render(request, 'auctions/language_test.html')

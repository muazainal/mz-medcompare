from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe

from .models import Medicine, LabReport, Manufacturer, Order
from .forms import MedicineForm, CustomSignupForm

stripe.api_key = settings.STRIPE_SECRET_KEY

# HOME PAGE
@login_required
def home(request):
    # --- Get query parameters from URL ---
    search_query = request.GET.get('search', '')  # search by medicine, manufacturer, formula
    rating = request.GET.get('rating')           # filter by rating
    sort = request.GET.get('sort')               # sort by price

    # --- Base Queryset ---
    if hasattr(request.user, 'manufacturer_profile'):
        medicines = Medicine.objects.filter(Q(is_paid=True) | Q(manufacturer=request.user.manufacturer_profile))
    else:
        medicines = Medicine.objects.filter(is_paid=True)

    # --- SEARCH ---
    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(manufacturer__name__icontains=search_query) |
            Q(formula__icontains=search_query) |
            Q(formulas__name__icontains=search_query)
        ).distinct()

    # --- FILTER ---
    if rating:
        medicines = medicines.filter(rating__gte=rating)

    # --- SORT ---
    if sort == 'price_asc':
        medicines = medicines.order_by('price')
    elif sort == 'price_desc':
        medicines = medicines.order_by('-price')

    # --- Render Template ---
    return render(
        request,
        'medicines/medicines_list.html',
        {'medicines': medicines}
    )

# DETAIL PAGE
@login_required
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(
        request,
        'medicines/medicine_detail.html',
        {'medicine': medicine}
    )

# SIGNUP/REGISTER
def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            
            if role == 'manufacturer':
                # Create Manufacturer profile
                name = form.cleaned_data.get('manufacturer_name')
                address = form.cleaned_data.get('manufacturer_address')
                Manufacturer.objects.create(user=user, name=name, address=address)
                
                # Add to Manufacturers group
                group, created = Group.objects.get_or_create(name='Manufacturers')
                user.groups.add(group)
            
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = CustomSignupForm()
    return render(request, 'registration/signup.html', {'form': form})

# MANUFACTURER DECORATOR
def manufacturer_required(view_func):
    def check_manufacturer(user):
        return user.groups.filter(name='Manufacturers').exists() or user.is_superuser
    return user_passes_test(check_manufacturer)(view_func)

# SUBMIT MEDICINE
@login_required
@manufacturer_required
def submit_medicine(request):
    try:
        manufacturer = request.user.manufacturer_profile
    except Manufacturer.DoesNotExist:
        messages.error(request, "Manufacturer profile not found.")
        return redirect('home')

    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.manufacturer = manufacturer
            medicine.save()

            pdf = request.FILES.get('lab_report')
            if pdf:
                LabReport.objects.create(medicine=medicine, pdf_file=pdf)

            messages.success(request, f"'{medicine.name}' has been submitted successfully!")
            return redirect('medicine_detail', pk=medicine.pk)
    else:
        form = MedicineForm()
    return render(request, 'medicines/submit_medicine.html', {'form': form})

# MY ORDERS
@login_required
def my_orders(request):
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'medicines/my_orders.html', {'orders': orders})

# --- STRIPE LOGIC ---
@login_required
@manufacturer_required
def create_checkout_session(request, medicine_id):
    try:
        medicine = Medicine.objects.get(id=medicine_id, manufacturer=request.user.manufacturer_profile)
    except Medicine.DoesNotExist:
        messages.error(request, "Medicine not found or access denied.")
        return redirect('home')
    
    if medicine.is_paid:
        messages.info(request, "This medicine is already published.")
        return redirect('medicine_detail', pk=medicine.id)

    domain_url = request.build_absolute_uri('/')[:-1]
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 5000, # $50.00 listing fee
                        'product_data': {
                            'name': f"Publish {medicine.name}",
                            'description': "One-time fee to publish medicine on MedCompare.",
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            metadata={'medicine_id': medicine.id},
            success_url=domain_url + '/payment-success/',
            cancel_url=domain_url + '/payment-cancel/',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f"Error creating checkout session: {str(e)}")
        return redirect('medicine_detail', pk=medicine.id)

def payment_success(request):
    messages.success(request, "Payment successful! Your medicine is now published.")
    return redirect('home')

def payment_cancel(request):
    messages.warning(request, "Payment was cancelled.")
    return redirect('home')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        import json
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        
        # Payment for Publishing Medicine (Manufacturer)
        medicine_id = session.get('metadata', {}).get('medicine_id')
        if medicine_id:
            try:
                medicine = Medicine.objects.get(id=medicine_id)
                medicine.is_paid = True
                medicine.save()
            except Medicine.DoesNotExist:
                pass
                
        # Payment for Buying Medicine (Standard User)
        purchase_medicine_id = session.get('metadata', {}).get('purchase_medicine_id')
        user_id = session.get('metadata', {}).get('user_id')
        if purchase_medicine_id and user_id:
            try:
                medicine = Medicine.objects.get(id=purchase_medicine_id)
                user = User.objects.get(id=user_id)
                
                # Extract shipping address
                shipping = session.get('shipping_details', {})
                address_parts = []
                if shipping and shipping.get('address'):
                    addr = shipping['address']
                    address_parts = [
                        shipping.get('name', ''),
                        addr.get('line1', ''),
                        addr.get('line2', ''),
                        addr.get('city', ''),
                        addr.get('state', ''),
                        addr.get('postal_code', ''),
                        addr.get('country', '')
                    ]
                
                shipping_address = ", ".join([p for p in address_parts if p])
                
                Order.objects.create(
                    user=user,
                    medicine=medicine,
                    stripe_checkout_id=session.get('id'),
                    amount=medicine.price,
                    shipping_address=shipping_address
                )
            except (Medicine.DoesNotExist, User.DoesNotExist):
                pass

    return HttpResponse(status=200)

@login_required
def create_purchase_session(request, medicine_id):
    try:
        medicine = Medicine.objects.get(id=medicine_id)
    except Medicine.DoesNotExist:
        messages.error(request, "Medicine not found.")
        return redirect('home')

    domain_url = request.build_absolute_uri('/')[:-1]
    
    # Ensure price is handled correctly (Stripe expects cents)
    unit_amount = int(medicine.price * 100)
    
    if unit_amount == 0:
        messages.error(request, "This medicine has no price set.")
        return redirect('medicine_detail', pk=medicine.id)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            shipping_address_collection={
                'allowed_countries': ['US', 'CA', 'GB', 'AU', 'MY'], # Example countries
            },
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': unit_amount,
                        'product_data': {
                            'name': f"Purchase {medicine.name}",
                            'description': f"Order for {medicine.name} from {medicine.manufacturer.name}.",
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            metadata={
                'purchase_medicine_id': medicine.id,
                'user_id': request.user.id
            },
            success_url=domain_url + '/purchase-success/',
            cancel_url=domain_url + '/purchase-cancel/',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f"Error creating purchase session: {str(e)}")
        return redirect('medicine_detail', pk=medicine.id)

def purchase_success(request):
    messages.success(request, "Order placed successfully! We have received your shipping details.")
    return redirect('home')

def purchase_cancel(request):
    messages.warning(request, "Order was cancelled.")
    return redirect('home')
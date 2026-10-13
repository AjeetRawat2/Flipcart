import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET, require_POST

from .catalog import CATEGORIES, PRODUCT_BY_SLUG, PRODUCTS, cart_lines, cart_total
from .models import Order

def _context(request, **extra):
    return {"categories": CATEGORIES, "cart_count": sum(request.session.get("cart", {}).values()), **extra}


@require_GET
def index(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "featured")
    products = PRODUCTS[:]
    if query:
        term = query.casefold()
        products = [p for p in products if term in p["name"].casefold() or term in p["category"].casefold() or term in p["description"].casefold()]
    if category in CATEGORIES:
        products = [p for p in products if p["category"] == category]
    if sort == "price_low":
        products.sort(key=lambda p: p["price"])
    elif sort == "price_high":
        products.sort(key=lambda p: p["price"], reverse=True)
    elif sort == "rating":
        products.sort(key=lambda p: float(p["rating"]), reverse=True)
    return render(request, "index.html", _context(request, products=products, query=query, selected_category=category, sort=sort))


@require_GET
def product_detail(request, slug):
    product = PRODUCT_BY_SLUG.get(slug)
    if product is None:
        raise Http404("That product could not be found.")
    related = [p for p in PRODUCTS if p["category"] == product["category"] and p["slug"] != slug][:4]
    return render(request, "product_detail.html", _context(request, product=product, related=related, is_wishlisted=slug in request.session.get("wishlist", [])))


@require_POST
def add_to_cart(request, slug):
    if slug not in PRODUCT_BY_SLUG:
        messages.error(request, "That product is no longer available.")
        return redirect("home")
    cart = request.session.get("cart", {})
    try:
        quantity = max(1, min(10, int(request.POST.get("quantity", "1") or 1)))
    except ValueError:
        quantity = 1
    cart[slug] = min(10, int(cart.get(slug, 0)) + quantity)
    request.session["cart"] = cart
    request.session.modified = True
    messages.success(request, "Added to your cart.")
    return redirect("cart")


@require_POST
def buy_now(request, slug):
    if slug not in PRODUCT_BY_SLUG:
        messages.error(request, "That product is no longer available.")
        return redirect("home")
    request.session["cart"] = {slug: 1}
    request.session.modified = True
    return redirect("checkout")


@require_GET
def cart(request):
    lines = cart_lines(request.session.get("cart", {}))
    subtotal = cart_total(lines)
    return render(request, "cart.html", _context(request, lines=lines, subtotal=subtotal, delivery=0 if subtotal >= 499 or not subtotal else 49, total=subtotal + (0 if subtotal >= 499 or not subtotal else 49)))


@require_POST
def update_cart(request, slug):
    cart_data = request.session.get("cart", {})
    if slug in cart_data:
        try:
            quantity = int(request.POST.get("quantity", "1"))
        except ValueError:
            quantity = 1
        if quantity <= 0:
            cart_data.pop(slug, None)
            messages.info(request, "Item removed from your cart.")
        else:
            cart_data[slug] = min(10, quantity)
    request.session["cart"] = cart_data
    return redirect("cart")


@require_POST
def toggle_wishlist(request, slug):
    if slug not in PRODUCT_BY_SLUG:
        return redirect("home")
    wishlist = request.session.get("wishlist", [])
    if slug in wishlist:
        wishlist.remove(slug)
        messages.info(request, "Removed from your saved items.")
    else:
        wishlist.append(slug)
        messages.success(request, "Saved to your wishlist.")
    request.session["wishlist"] = wishlist
    destination = request.POST.get("next", "")
    if destination and url_has_allowed_host_and_scheme(destination, allowed_hosts={request.get_host()}):
        return redirect(destination)
    return redirect("product_detail", slug=slug)


def signup(request):
    if request.user.is_authenticated:
        return redirect("account")
    next_url = request.POST.get("next") or request.GET.get("next", "")
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        if not name or len(name) > 150:
            messages.error(request, "Enter your name to continue.")
        else:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Enter a valid email address.")
            else:
                if User.objects.filter(username__iexact=email).exists() or User.objects.filter(email__iexact=email).exists():
                    messages.error(request, "An account already exists for that email. Please sign in.")
                elif len(password) < 8:
                    messages.error(request, "Choose a password with at least 8 characters.")
                else:
                    user = User.objects.create_user(username=email, email=email, password=password, first_name=name[:150])
                    login(request, user)
                    messages.success(request, "Your account is ready.")
                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        return redirect(next_url)
                    return redirect("account")
    return render(request, "auth.html", _context(request, mode="signup", next_url=next_url))


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("account")
    next_url = request.POST.get("next") or request.GET.get("next", "")
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        user = authenticate(request, username=email, password=request.POST.get("password", ""))
        if user is None:
            messages.error(request, "We couldn't sign you in. Check your email and password.")
        else:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("account")
    return render(request, "auth.html", _context(request, mode="login", next_url=next_url))


@require_POST
def sign_out(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("home")


@login_required
@require_GET
def account(request):
    orders = request.user.shop_orders.all()[:10]
    wishlist = [PRODUCT_BY_SLUG[s] for s in request.session.get("wishlist", []) if s in PRODUCT_BY_SLUG]
    return render(request, "account.html", _context(request, orders=orders, wishlist=wishlist))


def _checkout_context(request, **extra):
    lines = cart_lines(request.session.get("cart", {}))
    subtotal = cart_total(lines)
    delivery = 0 if subtotal >= 499 or not subtotal else 49
    return _context(request, lines=lines, subtotal=subtotal, delivery=delivery, total=subtotal + delivery,
                    demo_payment_enabled=True, **extra)


@login_required
def checkout(request):
    lines = cart_lines(request.session.get("cart", {}))
    if not lines:
        messages.info(request, "Your cart is empty.")
        return redirect("cart")
    if request.method == "POST":
        address = {key: request.POST.get(key, "").strip() for key in ("full_name", "phone", "address_line", "locality", "city", "state", "postal_code")}
        phone = address["phone"].replace("+", "").replace(" ", "").replace("-", "")
        if any(not address[key] for key in ("full_name", "phone", "address_line", "city", "state", "postal_code")) or not address["postal_code"].isdigit() or len(address["postal_code"]) != 6 or not phone.isdigit() or len(phone) < 10:
            messages.error(request, "Enter a complete delivery address and a valid Indian PIN code and phone number.")
            return render(request, "checkout.html", _checkout_context(request, address=address))
        method = request.POST.get("payment_method", "cod")
        if method == "cod":
            order = Order.objects.create(user=request.user, items=lines, total=Decimal(_checkout_context(request)["total"]), status="confirmed", payment_method="cod", shipping_address=address)
            request.session["cart"] = {}
            messages.success(request, "Order placed. Pay when it arrives.")
            return redirect("order_detail", pk=order.pk)
        if method == "demo":
            return render(request, "checkout.html", _checkout_context(request, address=address, start_online_payment=True))
        messages.error(request, "Choose a checkout option to continue.")
    return render(request, "checkout.html", _checkout_context(request, address={"full_name": request.user.first_name}))


@login_required
@require_POST
def create_payment_order(request):
    lines = cart_lines(request.session.get("cart", {}))
    if not lines:
        return JsonResponse({"error": "Your cart is empty."}, status=400)
    try:
        body = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid checkout details."}, status=400)
    address = body.get("address", {})
    required = ("full_name", "phone", "address_line", "locality", "city", "state", "postal_code")
    must_have = ("full_name", "phone", "address_line", "city", "state", "postal_code")
    if not isinstance(address, dict) or any(not str(address.get(k, "")).strip() for k in must_have):
        return JsonResponse({"error": "Complete the delivery address first."}, status=400)
    phone = str(address["phone"]).replace("+", "").replace(" ", "").replace("-", "")
    postal_code = str(address["postal_code"])
    if not phone.isdigit() or len(phone) < 10 or not postal_code.isdigit() or len(postal_code) != 6:
        return JsonResponse({"error": "Enter a valid phone number and 6-digit PIN code."}, status=400)
    subtotal = cart_total(lines)
    total = subtotal + (0 if subtotal >= 499 else 49)
    order = Order.objects.create(user=request.user, items=lines, total=Decimal(total), status="pending", payment_method="demo", shipping_address={k: str(address[k]).strip() for k in required})
    return JsonResponse({"store_order_id": order.pk, "amount": total, "currency": "INR", "demo": True})


@login_required
@require_POST
def verify_payment(request):
    try:
        body = json.loads(request.body or "{}")
        order = Order.objects.get(pk=int(body.get("store_order_id")), user=request.user, payment_method="demo", status="pending")
    except (json.JSONDecodeError, TypeError, ValueError, Order.DoesNotExist, AttributeError):
        return JsonResponse({"error": "We couldn't find that order."}, status=404)
    if not isinstance(body, dict) or body.get("confirmed") is not True:
        return JsonResponse({"error": "No demo confirmation was received."}, status=400)
    order.payment_id = "DEMO-PAYMENT"
    order.status = "confirmed"
    order.save(update_fields=["payment_id", "status"])
    request.session["cart"] = {}
    return JsonResponse({"redirect": reverse("order_detail", kwargs={"pk": order.pk}), "demo": True})


@login_required
@require_POST
def cancel_demo_payment(request):
    try:
        body = json.loads(request.body or "{}")
        order = Order.objects.get(pk=int(body.get("store_order_id")), user=request.user, payment_method="demo", status="pending")
    except (json.JSONDecodeError, TypeError, ValueError, Order.DoesNotExist, AttributeError):
        return JsonResponse({"ok": True})
    order.delete()
    return JsonResponse({"ok": True})


@login_required
@require_GET
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "order_detail.html", _context(request, order=order))

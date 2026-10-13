from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("check", views.product_detail, {"slug": "samsung-galaxy-s24-fe"}, name="check"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("buy/<slug:slug>/", views.buy_now, name="buy_now"),
    path("cart/update/<slug:slug>/", views.update_cart, name="update_cart"),
    path("wishlist/<slug:slug>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("account/login/", views.sign_in, name="login"),
    path("account/signup/", views.signup, name="signup"),
    path("account/logout/", views.sign_out, name="logout"),
    path("account/", views.account, name="account"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/demo-payment/", views.create_payment_order, name="create_payment_order"),
    path("checkout/demo-payment/complete/", views.verify_payment, name="verify_payment"),
    path("checkout/demo-payment/cancel/", views.cancel_demo_payment, name="cancel_demo_payment"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
]

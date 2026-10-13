"""Small starter catalogue. Product prices are always resolved on the server."""

PRODUCTS = [
    {"slug":"samsung-galaxy-s24-fe","name":"Samsung Galaxy S24 FE 5G","category":"Mobiles","price":44999,"mrp":59999,"rating":"4.4","reviews":"12,840","badge":"Bestseller","image":"https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=85","description":"A vivid AMOLED display, versatile camera system and all-day battery, wrapped in a refined Galaxy design."},
    {"slug":"iphone-15","name":"Apple iPhone 15 (128 GB)","category":"Mobiles","price":58999,"mrp":69900,"rating":"4.6","reviews":"8,211","badge":"Top rated","image":"https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=900&q=85","description":"A powerful, pocket-friendly phone with a brilliant display and an advanced dual-camera system."},
    {"slug":"sony-wireless-headphones","name":"Sony WH-CH720N Wireless Headphones","category":"Electronics","price":7490,"mrp":14990,"rating":"4.3","reviews":"3,807","badge":"Deal of the day","image":"https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=85","description":"Comfortable wireless listening with rich sound and noise cancelling for commutes and focus time."},
    {"slug":"smart-watch-active","name":"Noise ColorFit Pro 5 Smartwatch","category":"Electronics","price":2999,"mrp":5999,"rating":"4.2","reviews":"2,122","badge":"Hot deal","image":"https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=85","description":"A bright smart display with health tracking, workout modes and useful everyday notifications."},
    {"slug":"classic-cotton-tee","name":"Men's Classic Fit Cotton T-shirt","category":"Fashion","price":499,"mrp":999,"rating":"4.1","reviews":"1,290","badge":"Popular","image":"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=85","description":"An easy everyday essential in soft cotton, finished with a comfortable classic fit."},
    {"slug":"everyday-sneakers","name":"Everyday Low-Top Sneakers","category":"Fashion","price":1599,"mrp":3499,"rating":"4.0","reviews":"947","badge":"40% off","image":"https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=85","description":"Lightweight, versatile sneakers designed for comfortable walks and casual days out."},
    {"slug":"air-fryer-4l","name":"4 L Digital Air Fryer","category":"Home","price":4999,"mrp":8999,"rating":"4.3","reviews":"663","badge":"Great value","image":"https://images.unsplash.com/photo-1585515320310-259814833e62?auto=format&fit=crop&w=900&q=85","description":"Make crisp favourites with less oil using simple digital controls and an easy-clean basket."},
    {"slug":"ceramic-dinner-set","name":"Stoneware Dinner Set, 16 Pieces","category":"Home","price":2299,"mrp":3999,"rating":"4.2","reviews":"512","badge":"New arrival","image":"https://images.unsplash.com/photo-1603199506016-b9a594b593c0?auto=format&fit=crop&w=900&q=85","description":"A modern, durable stoneware set that brings a warm handmade touch to the table."},
    {"slug":"travel-backpack","name":"Urban Trail Laptop Backpack","category":"Travel","price":1299,"mrp":2499,"rating":"4.1","reviews":"1,104","badge":"Bestseller","image":"https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=85","description":"A roomy, organized backpack with a padded laptop sleeve for work, class and short trips."},
    {"slug":"bestseller-paperbacks","name":"Bestselling Fiction Collection (Set of 3)","category":"Books","price":699,"mrp":1199,"rating":"4.5","reviews":"388","badge":"Readers' pick","image":"https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=900&q=85","description":"Three page-turning contemporary stories, selected for readers who love a great weekend read."},
    {"slug":"skin-care-set","name":"Daily Skin Care Essentials Set","category":"Beauty","price":899,"mrp":1499,"rating":"4.2","reviews":"734","badge":"Value pack","image":"https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=900&q=85","description":"A gentle daily routine set with lightweight essentials for a fresh, comfortable feel."},
    {"slug":"portable-bluetooth-speaker","name":"Portable Bluetooth Speaker","category":"Electronics","price":1899,"mrp":3499,"rating":"4.4","reviews":"2,045","badge":"Top rated","image":"https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=900&q=85","description":"Big, clear sound in a compact wireless speaker made for home listening and weekends away."},
]

PRODUCT_BY_SLUG = {product["slug"]: product for product in PRODUCTS}
CATEGORIES = ["Mobiles", "Electronics", "Fashion", "Home", "Travel", "Books", "Beauty"]


def cart_lines(cart):
    lines = []
    for slug, quantity in cart.items():
        product = PRODUCT_BY_SLUG.get(slug)
        if not product:
            continue
        quantity = max(1, min(10, int(quantity)))
        lines.append({**product, "quantity": quantity, "line_total": product["price"] * quantity})
    return lines


def cart_total(lines):
    return sum(line["line_total"] for line in lines)

from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect
from firstapp.models import Category, Product, CartItem, Cart

# Create your views here.
def page_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id )
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    cart = Cart.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'cart': cart
    }
    return render(request, 'page.html', context)

def product_view(request, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id )
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'cart': cart
    }
    return render(request, 'product.html', context)

def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products_of_category = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products_of_category': products_of_category
    }
    return render(request, 'category.html', context)

def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id )
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'cart': cart
    }
    return render(request, 'cart.html', context)

def add_to_cart_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id )
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    if new_item not in cart.items.all():
        cart.items.add(new_item)
        cart.save()
        return HttpResponseRedirect('/cart/')

def remove_from_cart_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
    cart = Cart.objects.first()
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id )
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    for cart_item in cart.items.all():
        if cart_item.product == product:
            cart.items.remove(cart_item)
            cart.save()
            return HttpResponseRedirect('/cart/')
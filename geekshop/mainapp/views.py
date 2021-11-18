from django.shortcuts import render


def main(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    context = {
        'title': 'GeekShop-Каталог',
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html')

def test_content(request):
    context = {
        'title': 'GeekShop',
        'header': 'Welcome friendo',
        'user': 'loser',
        'products': [
            { 'name': 'Hoody', 'price': 7899 },
            {'name': 'Blue jaket', 'price': 1899},
            {'name': 'Nike', 'price': 3800},
            {'name': 'Bex Black', 'price': 900},

        ]
    }
    return render(request, 'mainapp/test_content.html', context)

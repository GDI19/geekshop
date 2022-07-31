"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from mainapp.views import index #, contact
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('', index, name='index'),
    path('products/',  include('mainapp.urls', namespace='mainapp')),
    # path('contact/', contact,),
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('admins/', include('admins.urls', namespace='admins')),
    path('orders/', include('ordersapp.urls', namespace='orders')),
    path('', include('social_django.urls', namespace='social')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# для того чтобы статика не кешировалась использовать при runserver --nostatic
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, view=cache_control(no_cache=True, must_revalidate=True)(serve))
# другой способ не кэшировать
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, view=never_cache(serve))

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

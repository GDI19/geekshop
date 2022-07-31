from django.urls import path, re_path
import authapp.views as authapp
from authapp.views import LoginListView, Logout, ProfileFormView

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', authapp.register, name='register'),
    path('profile/', ProfileFormView.as_view(), name='profile'),
    # re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify')
    path('verify/<str:email>/<str:activation_key>/', authapp.verify, name='verify')
]
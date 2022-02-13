from django.urls import path
import authapp.views as authapp
from authapp.views import LoginListView, Logout, RegisterListView, ProfileFormView

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterListView.as_view(), name='register'),
    path('profile/', ProfileFormView.as_view(), name='profile'),

    # path('verify/<str:email>/<str:activate_key>/', RegisterListView.verify, name='verify')
]
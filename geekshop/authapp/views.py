from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfilerForm

from basketapp.models import Basket


def login(request):
    title = 'GeekShop - Вход'

    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))

    else:
        # login_form = UserLoginForm()
        content = {'title': title, 'login_form': login_form}
        return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = UserRegisterForm(data=request.POST)

        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            print(register_form.errors)
    else:
        register_form = UserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


@login_required
# для перенаправления на другую стр.(назначается в settings LOGIN_URL='/auth/login')
# если юзер не  залогиненый
def profile(request):
    title = 'Профиль'

    if request.method == 'POST':
        edit_form = UserProfilerForm(data=request.POST,files=request.FILES, instance=request.user)
        if edit_form.is_valid():
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Вы успешно сохранили профайл')
            edit_form.save()
            # return HttpResponseRedirect(reverse('authapp:profile'))
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, edit_form.errors)
    else:
        edit_form = UserProfilerForm(instance=request.user)

    content = {
        'title': title,
        'edit_form': edit_form,
        'baskets': Basket.objects.filter(user=request.user),
    }

    return render(request, 'authapp/profile.html', content)

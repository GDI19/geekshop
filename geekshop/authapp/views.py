from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib import messages, auth
from django.urls import reverse, reverse_lazy

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfilerForm
from basketapp.models import Basket
from django.views.generic import FormView, UpdateView
from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin

from authapp.models import User

from authapp.forms import UserProfileEditForm


class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Вход'


class Logout(LogoutView):
    template_name = 'mainapp/index.html'


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} ' \
              f'на портале {settings.DOMAIN_NAME} ' \
              f'перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = UserRegisterForm(data=request.POST)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                # print('сообщение подтверждения отправлено')
                messages.success(request, 'Вы успешно зарегистрировались, вам была отправлена ссылка на почту'
                                          ' подтвердите свой  аккаунт перейдя по ссылке')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                # print('ошибка отправки сообщения')
                messages.success(request, 'Ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
        else:
            # print(register_form.errors)
            messages.set_level(request, messages.ERROR)
            messages.error(request, register_form.errors)
            register_form = UserRegisterForm(data=request.POST, files=request.FILES)
    else:
        register_form = UserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            # Уточним процесс аутентификации пользователя при вызове метода auth.login() явно зададим бэкенд:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    template_name = 'authapp/profile.html'
    form_class = UserProfilerForm
    success_url = reverse_lazy('authapp:profile')
    title = 'GeekShop - Профиль'

    def post(self, request, *args, **kwargs):
        form = UserProfilerForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
        return redirect(self.success_url)

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, "Вы успешно обновили информацию")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.shopuserprofile)
        # context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context


"""
class RegisterListView(FormView, BaseClassContextMixin):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    title = 'GeekShop - Регистрация'
    success_url = reverse_lazy('auth:login')

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Вы успешно зарегистрировались!')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, form.errors)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})

    def send_verify_link(self, user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username}  на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activate_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user)
            return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))
"""

"""
@login_required
# для перенаправления на другую стр.(назначается в settings LOGIN_URL='/auth/login') если юзер не  залогиненый
@transaction.atomic
# для атомарности т.е. при ошибке в трансзакции действие откатывается до начального состояния
def profile(request):
    title = 'Профиль'

    if request.method == 'POST':
        edit_form = UserProfilerForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Вы успешно сохранили профайл')
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:profile'))
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, edit_form.errors)
            edit_form = UserProfilerForm(instance=request.user)
            profile_form = UserProfileEditForm(instance=request.user.shopuserprofile)
    else:
        edit_form = UserProfilerForm(instance=request.user)

    content = {
        'title': title,
        'edit_form': edit_form,
        'baskets': Basket.objects.filter(user=request.user),
        'profile_form': profile_form,
    }

    return render(request, 'authapp/profile.html', content)
    
"""

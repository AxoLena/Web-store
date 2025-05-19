from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import auth, messages
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, TemplateView
from django.core.cache import cache
from django.core.mail import send_mail

from store import settings
from users.forms import UserLoginForm, UserRegForm, UserProfileForm, UserPasswordResetFrom
from carts.models import Cart
from orders.models import Order, OrderItem
from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f'{user.username}, Вы были авторизованы')
                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - вход'
        return context


class UserRegView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance
        if user:
            form.save()
            auth.login(self.request,user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
        messages.success(self.request, f'{user.username}, Вы были успешно зарегестрированы и вошли в аккаунт')
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - регистрация'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль был обновлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - личный кабинет'

        orders = cache.get(f'orders_for_user_{self.request.user.id}')
        if not orders:
            orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch('orderitem_set',queryset=OrderItem.objects.select_related('product'))).order_by('-id')
            cache.set(f'orders_for_user_{self.request.user.id}', orders, 60)

        context['orders'] = orders
        return context


@login_required
def logout(request):
    messages.success(request, f'{request.user.username}, Вы вышли из аккаунта')
    auth.logout(request)
    return redirect(reverse('main:index'))


class PasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = UserPasswordResetFrom
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = self.request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.success(self.request, 'Письмо с инструкцией по восстановлению пароля отправлена на ваш эл. адресс')
            email_template_name = 'users/email/password_reset_email.html'
            subject = 'Восстановление пароля'
            token_generator = default_token_generator
            current_site = get_current_site(self.request)
            user = User.objects.get(email=email)
            message = render_to_string(email_template_name, {
                'request': self.request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], html_message=message)
            return redirect(reverse_lazy('users:login'))
        else:
            messages.warning(self.request, 'Пользователя с такой почтой не существует')
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HOMAGE - восстановление пароля'
        return context


class SetNewPasswordView(PasswordResetConfirmView):
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        password = self.request.POST.get('new_password1')
        if self.user.password == password:
            self.user.password = form.new_password1
            self.user.save()
            messages.success(self.request, 'Пароль успешно изменен! Можете авторизоваться на сайте')
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'Пароль не удалось изменить: введенный пароль совпадает с предыдущим')
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'fdjahfjda'
        return context


class UserCartView(TemplateView):
    template_name = 'users/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - корзина'
        return context

from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.UserRegView.as_view(), name='reg'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/set-new-password/<uidb64>/<token>/', views.SetNewPasswordView.as_view(), name='password_reset_confirm'),
    path('users-cart/', views.UserCartView.as_view(), name='users_cart')
]
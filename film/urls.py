from  django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name = 'home'),

    path('register/',views.registerPage,name='register'),
    path('login',views.loginPage,name='login'),
    path('logout',views.logoutUser,name='logout'),
    

    path('products/',views.products,name='products'),
    path('customer/<str:pk>/',views.customer,name='customer'),

    path('create_order/<str:pk>/',views.createOrder,name='create_order'),
      path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
      path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),
      path('user/',views.userPage,name='user-page'),
      path('account',views.accountSettings,name="account"),

      path('reset_password/',auth_views.PasswordResetView.as_view
      (),name='reset_password'),

       path('password-reset/done/',auth_views.PasswordResetDoneView.as_view
       (),name= 'password_reset_done'),

        path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view
        (),name='password_reset_confirm'),
         path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view
         (),name='password_reset_complete'),
]

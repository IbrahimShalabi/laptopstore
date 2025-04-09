from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.home,name='home'),
    path('laptops/',views.laptops,name='laptops'),
    path('customer/<str:pk>',views.customer,name='customer'),
    path('create/<str:pk>',views.create,name='create'),
    path('update/<int:pk>/', views.update_order, name='update_order'),
    path('delete/<str:pk>',views.delete,name='delete'),
    path('login/',views.userlogin,name='login'),
    path('logout/',views.userlogout,name='logout'),
    path('register/',views.register,name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('profile_info/', views.profile_info, name='profile_info'),
    path('add_laptop/', views.add_laptop, name='add_laptop'),
    path('laptop/<int:pk>/', views.laptop_detail, name='laptop_detail'),
    path('favorites/', views.favorite_laptops, name='favorite_laptops'),
    path('add-to-favorites/<int:laptop_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:laptop_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('add_to_invoice/<int:laptop_id>/', views.add_to_invoice, name='add_to_invoice'),
    path('delivery_information/', views.delivery_information, name='delivery_information'),
    path('about_us/', views.about_us, name='about_us'),
    path('our_team/', views.our_team, name='our_team'),
    path('contact/', views.contact_us, name='contact_us'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('make_admin/', views.make_admin, name='make_admin'),
    path('remove_admin/', views.remove_admin, name='remove_admin'),
    path('user_behavior_analysis/', views.user_behavior_analysis, name='user_behavior_analysis'),



        
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="laptopstore/reset_password.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="laptopstore/reset_password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="laptopstore/reset_password_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="laptopstore/reset_password_done.html"), name='password_reset_complete'),


     
]

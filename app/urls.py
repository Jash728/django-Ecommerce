from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import  MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('app/search/', views.search, name='search'),
    path('address/', views.address, name='address'),
    path('addr/', views.AddressView.as_view(), name='addr'),
    path('orders/', views.orders, name='orders'),
    path('product//<int:pk>', views.ProductDetailView.as_view(), name='product-detail' ),
    path('app/order_confirmation/', views.orderconfirmation, name='order_confirmation'),
    path('category/<category>/', views.CatListView.as_view(), name='category'),
    path('category/<category>', views.CatListView.as_view(), name='category'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('remove-coupon/<cart_id>/', views.remove_coupon, name = "remove_coupon"),
    path('coupon-code/', views.coupon_code, name = 'coupon_code' ),

    # User Registration
    path("signin/", views.signin, name="login"),
    path('registration/', views.RegistrationUserView.as_view(), name='signup'),
    path('accounts/login/', auth_views.LogoutView.as_view(next_page = 'login'), name='logout'),
    path("success/", TemplateView.as_view(template_name="app/success.html"), name="success"),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name = 'app/passwordchange.html', form_class = MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name = 'app/passwordchangedone.html'), 
    name='passwordchangedone'), 
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'app/password_reset_confirm.html', form_class = MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'app/password_reset_complete.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

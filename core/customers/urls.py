# RegisterView

from django.urls import path


from core.customers.views import *
urlpatterns = [
    path('customer/register/', RegisterView.as_view(), name='register_user'),
    path('get/current/user', UserProfileView.as_view(), name='current_user'),
    path('users/', UserListView.as_view(), name='all_user'),
    path('users/customers/', CustomerUserListView.as_view(), name='Customers_user'),

]
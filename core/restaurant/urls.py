from django.urls import path
from core.restaurant.endpoints.restaurants.views import RestaurantListAPIView, RestaurantRetrieveAPIView
from core.restaurant.endpoints.tables.views import TableListCreateView, TableRetrieveUpdateDestroyAPIView, \
    TableSummaryApiView,TableByRestaurant

urlpatterns = [
    path('restaurant/', RestaurantListAPIView.as_view()),
    path('restaurant/<int:pk>/', RestaurantRetrieveAPIView.as_view()),
    path('table/', TableListCreateView.as_view()),
    path('table/<int:pk>/restaurant/', TableByRestaurant.as_view()),
    path('table/<int:restaurant_id>/table-summary/', TableSummaryApiView.as_view(), name='table-summary'),
    path('table/<int:pk>/', TableRetrieveUpdateDestroyAPIView.as_view()),

]

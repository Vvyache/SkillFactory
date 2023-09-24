from django.urls import path
from .views import SignUp, LogoutView #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from django.urls import reverse_lazy

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Добавил !!!!!!!!!!!!!!!!!!!!
]
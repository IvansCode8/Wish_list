"""wish_list_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from wish_list_app import views # <-- this part is new

urlpatterns = [
    path('', views.index), # <-- this part is new
    path('reset/', views.reset), # <-- this part is new
    path('wish_items/reset/', views.reset), # <-- this part is new
    path('main', views.main), # <-- this part is new
    path('login', views.login), # <-- this part is new
    path('register', views.register), # <-- this part is new
    path('dashboard', views.dashboard), # <-- this part is new
    path('wish_items/create', views.create), # <-- this part is new
    path('AddItem', views.AddItem), # <-- this part is new
    path('wish_items/<id>', views.show), # <-- this part is new
    path('AddToWishlist/<id>', views.AddToWishlist), # <-- this part is new
    path('RemoveFromWishlist/<id>', views.RemoveFromWishlist), # <-- this part is new
    path('Delete/<id>', views.remove), # <-- this part is new

]
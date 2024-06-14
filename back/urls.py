"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from poate.views import Cards, LoginView, Idk, Meditations, Sounds, Yoga

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("api/", create_data),
    # path("with_imgs/", create_data_with_img),
    # path("a/", upload_images),  
    # path('getIt/', getIt),      
    # path('testIt/', testIt),
    
    path('idk/', Idk.as_view(), name='Idk'),

    path('login/', LoginView.as_view(), name='login'),
    path('register/', LoginView.as_view(), name='register'),
    
    path('meditations/', Meditations.as_view({'get':'list'})),
    path('meditations/create', Meditations.as_view({'post':'create'})),
    path('meditations/<str:pk>/delete', Meditations.as_view({'delete':'destroy'})),
    path('meditations/<str:pk>/details/', Meditations.as_view({'get':'retrieve'})),
    path('meditations/<str:pk>/category/', Meditations.as_view({'get':'get_by_cat'})),


    path('cards/', Cards.as_view({'get':'list'})),
    path('cards/create', Cards.as_view({'post':'create'})),
    path('cards/<str:pk>/delete', Cards.as_view({'delete':'destroy'})),
    path('cards/<str:pk>/details/', Cards.as_view({'get':'retrieve'})),

    path('sounds/', Sounds.as_view({'get':'list'})),
    path('sounds/create', Sounds.as_view({'post':'create'})),
    path('sounds/<str:pk>/delete', Sounds.as_view({'delete':'destroy'})),
    path('sounds/<str:pk>/details/', Sounds.as_view({'get':'retrieve'})),
    path('sounds/<str:pk>/category/', Sounds.as_view({'get':'get_by_cat'})),
    
    
    path('yoga/', Yoga.as_view({'get':'list'})),
    path('yoga/create', Yoga.as_view({'post':'create'})),
    path('yoga/<str:pk>/delete', Yoga.as_view({'delete':'destroy'})),
    path('yoga/<str:pk>/details/', Yoga.as_view({'get':'retrieve'})),
]

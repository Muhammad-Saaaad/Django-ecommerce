from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # for getting the jwt token

from home.views import *

user_router = DefaultRouter()
user_router.register('User', UserMvs, basename='User api')

urlpatterns=[
    path('User-register', RegisterUser.as_view()),
    path('User-login', LoginUser.as_view()),
    path('User-api', include(user_router.urls)),
    path("product-api", ProductCb.as_view()),
    # path(('jwt-token'), TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("like-product", ProductLike.as_view()),
    path('add-to-cart-product', AddToCart.as_view())
]

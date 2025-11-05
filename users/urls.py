from django.urls import path
from .views import LoginAPI, LogoutAPI, LogoutAllAPI, RegisterAPI, VerifyOtpAPI

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('logoutall/', LogoutAllAPI.as_view(), name='logoutall'),
    path("register/", RegisterAPI.as_view(), name="register"),
    path("verify-otp/", VerifyOtpAPI.as_view(), name="verify-otp"),
]

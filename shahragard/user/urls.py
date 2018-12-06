from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from . import views

urlpatterns = [
    path('apiv1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('apiv1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('apiv1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('apiv1/user/', views.UserHandler.as_view()),
]
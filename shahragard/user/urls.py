from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

urlpatterns = [
    path('apiv1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
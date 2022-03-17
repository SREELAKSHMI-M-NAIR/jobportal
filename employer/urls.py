from employer import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from django.urls import path
router = DefaultRouter()
router.register('company', views.CompanyViewSet, basename='company')
router.register('candidate', views.CandidateViewSet, basename='candidate'),
router.register('jobs', views.JobViewSet, basename='jobs')


urlpatterns=[
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]+router.urls
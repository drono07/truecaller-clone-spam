from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SpamReportViewSet, ContactListViewSet, UserLoginView, UserLogoutView, SearchByNameView, SearchByNumberView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'spamreports', SpamReportViewSet)
router.register(r'contactlists', ContactListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('search/name/<str:name>/', SearchByNameView.as_view(), name='search-by-name'),
    path('search/number/<str:number>/', SearchByNumberView.as_view(), name='search-by-number'),
]

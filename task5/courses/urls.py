from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'courses', views.CoursesViewSet, basename='courses')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('lectures/', views.LecturesListView.as_view(), name='lectures_list'),
    path('lectures/<int:pk>/', views.LecturesDetailView.as_view(), name='lectures_detail'),
    path('homework/', views.HomeworkListView.as_view(), name='homework_list'),
    path('homework/<int:pk>/', views.HomeworkDetailView.as_view(), name='homework_detail'),
]

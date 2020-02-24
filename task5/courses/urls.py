from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('courses/', views.CoursesListView.as_view(), name='courses_list'),
    path('courses/<int:pk>/', views.CoursesDetailView.as_view(), name='courses_detail'),
    path('courses/<int:pk>/students/', views.CoursesStudentsListView.as_view(), name='courses_students_list'),
    path('courses/<int:pk>/professors/', views.CoursesProfessorsListView.as_view(), name='courses_professors_list'),
]

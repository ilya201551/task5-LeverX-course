from django.urls import path, include
from .Users import views as users_views
from .Courses import views as courses_views
from .Lectures import views as lectures_views
from .Homework import views as homework_views
from .Solutions import views as solution_views
from .Mark import views as mark_views
from .Comments import views as comments_views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', users_views.UserViewSet)
router.register(r'courses', courses_views.CoursesViewSet, basename='courses')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', users_views.UserRegistrationView.as_view(), name='user_register'),
    path('login/', users_views.UserLoginView.as_view(), name='user_login'),
    path('logout/', users_views.UserLogoutView.as_view(), name='user_logout'),
    path('lectures/', lectures_views.LecturesListView.as_view(), name='lectures_list'),
    path('lectures/<int:pk>/', lectures_views.LecturesDetailView.as_view(), name='lectures_detail'),
    path('homework/', homework_views.HomeworkListView.as_view(), name='homework_list'),
    path('homework/<int:pk>/', homework_views.HomeworkDetailView.as_view(), name='homework_detail'),
    path('solutions/', solution_views.SolutionListView.as_view(), name='solutions_list'),
    path('solutions/<int:pk>/', solution_views.SolutionDetailView.as_view(), name='solutions_detail'),
    path('marks/', mark_views.MarkListView.as_view(), name='marks_list'),
    path('marks/<int:pk>/', mark_views.MarkDetailView.as_view(), name='marks_detail'),
    path('comments/', comments_views.CommentListView.as_view(), name='comments_list'),
    path('comments/<int:pk>/', comments_views.CommentDetailView.as_view(), name='comments_detail'),
]

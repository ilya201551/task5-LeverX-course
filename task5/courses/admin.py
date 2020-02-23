from django.contrib import admin
from .models import (AdvUser,
                     Lecture,
                     Homework,
                     Course,
                     FinishedHomework,
                     Comment,
                     )


@admin.register(AdvUser)
class AdvUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    pass


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(FinishedHomework)
class FinishedHomeworkAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

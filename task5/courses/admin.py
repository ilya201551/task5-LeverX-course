from django.contrib import admin
from .models import (AdvUser,
                     Lecture,
                     Homework,
                     Course,
                     Mark,
                     Solution,
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


@admin.register(Mark)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

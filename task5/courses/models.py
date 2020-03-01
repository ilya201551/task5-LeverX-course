from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    status = models.CharField(max_length=10,
                              choices=[('S', 'Student'),
                                       ('P', 'Professor')],
                              blank=False)

    class Meta(AbstractUser.Meta):
        pass


class Course(models.Model):
    owner = models.ForeignKey(AdvUser,
                              on_delete=models.CASCADE,
                              blank=False)
    name = models.CharField(max_length=100,
                            blank=False)
    students = models.ManyToManyField(AdvUser,
                                      related_name='students_set')
    professors = models.ManyToManyField(AdvUser,
                                        related_name='professors_set')

    def __str__(self):
        return f'{self.name}'


class Lecture(models.Model):
    owner = models.ForeignKey(AdvUser,
                              on_delete=models.CASCADE,
                              blank=False)
    topic = models.CharField(max_length=100,
                             blank=False)
    presentation = models.FileField(upload_to='uploads/%Y/%m/%d/',
                                    blank=True)
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               blank=False,
                               related_name='lectures')

    def __str__(self):
        return f'{self.topic}'


class Homework(models.Model):
    owner = models.ForeignKey(AdvUser,
                              on_delete=models.CASCADE,
                              blank=False)
    task = models.TextField(blank=False)
    lecture = models.ForeignKey(Lecture,
                                on_delete=models.CASCADE,
                                blank=False,
                                related_name='tasks')

    def __str__(self):
        return f'{self.task}'


class Solution(models.Model):
    link = models.CharField(max_length=150,
                            blank=True)
    finished = models.BooleanField(blank=False,
                                   default=False)
    owner = models.ForeignKey(AdvUser,
                              on_delete=models.CASCADE,
                              blank=False)
    homework = models.ForeignKey(Homework,
                                 on_delete=models.CASCADE,
                                 blank=False,
                                 related_name='solution')

    def __str__(self):
        return f'{self.link}'


class Mark(models.Model):
    value = models.SmallIntegerField(blank=False)
    owner = models.ForeignKey(AdvUser,
                              on_delete=models.CASCADE,
                              blank=False)
    solution = models.OneToOneField(Solution,
                                    on_delete=models.CASCADE,
                                    blank=False,
                                    related_name='mark')

    def __str__(self):
        return f'Mark - {self.value}'


class Comment(models.Model):
    text = models.TextField(blank=False)
    owner = models.ForeignKey(AdvUser,
                              blank=False,
                              on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark,
                             on_delete=models.CASCADE,
                             blank=False,
                             related_name='comments')

    def __str__(self):
        return f'{self.text}'

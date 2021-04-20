from django.contrib import admin
from django.db import models

from polls.models import Answer, Poll, Question, CompletedPoll, UserAnswer


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time')
    inlines = (QuestionInline,)


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'poll')
    inlines = (AnswerInline,)


class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0


@admin.register(CompletedPoll)
class CompletedPollAdmin(admin.ModelAdmin):
    inlines = (UserAnswerInline,)

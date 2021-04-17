from django.contrib import admin

from polls.models import Answer, Poll, Question


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

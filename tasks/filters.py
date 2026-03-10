import django_filters
from django import forms
from django.contrib.auth.models import User

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Статус",
        empty_label="---------",
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Исполнитель",
        empty_label="---------",
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label="Метка",
        empty_label="---------",
        method="filter_labels",
    )
    self_tasks = django_filters.BooleanFilter(
        label="Только свои задачи",
        method="filter_self_tasks",
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]

    def filter_labels(self, queryset, name, value):
        if value:
            return queryset.filter(labels=value)
        return queryset

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

from django import forms
from django.contrib.auth.models import User

from tasks.models import Task


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = obj.get_full_name()
        return full_name if full_name else obj.username


class TaskForm(forms.ModelForm):
    executor = UserChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Исполнитель",
    )

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
        error_messages = {
            "name": {
                "unique": "Задача с таким именем уже существует"
            }
        }

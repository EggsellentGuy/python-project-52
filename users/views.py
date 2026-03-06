from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages

from users.forms import UserRegisterForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/form.html"
    success_url = reverse_lazy("login")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/form.html"
    success_url = reverse_lazy("users:index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            messages.error(
                request, "You have no permission to change another user.")
            return redirect("users:index")
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            messages.error(
                request, "You have no permission to delete another user.")
            return redirect("users:index")
        return super().dispatch(request, *args, **kwargs)

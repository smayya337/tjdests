from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from tjdests.apps.authentication.decorators import require_accept_tos
from tjdests.apps.destinations.models import Decision, TestScore

from .forms import DecisionForm, ProfilePublishForm, TestScoreForm


@login_required
@require_accept_tos
def profile_view(request: HttpRequest):
    # mypy is annoying.
    test_scores = TestScore.objects.filter(user=request.user)  # type: ignore
    decisions = Decision.objects.filter(user=request.user)  # type: ignore

    # A POST request would mean that the user is saving their profile publication status
    if request.method == "POST":
        profile_form = ProfilePublishForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()

            messages.success(request, "Your preferences have been changed.")
    else:
        profile_form = ProfilePublishForm(instance=request.user)

    context = {
        "test_scores_list": test_scores,
        "decisions_list": decisions,
        "profile_form": profile_form,
    }

    return render(request, "profile/profile.html", context=context)


class TestScoreCreateView(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView
):
    model = TestScore
    form_class = TestScoreForm
    template_name = "profile/testscore_form.html"
    success_message = "Test score created successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        assert self.request.user.is_authenticated
        return self.request.user.can_update_profile and self.request.user.accepted_terms

    def get_success_url(self):
        return reverse("profile:index")


class TestScoreUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView
):
    model = TestScore
    form_class = TestScoreForm
    template_name = "profile/testscore_form.html"
    success_message = "Test score updated successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        assert self.request.user.is_authenticated
        owner = self.request.user
        return self.model.objects.filter(user=owner)

    def test_func(self):
        assert self.request.user.is_authenticated
        return self.request.user.can_update_profile and self.request.user.accepted_terms

    def get_success_url(self):
        return reverse("profile:index")


class TestScoreDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView
):
    object: TestScore
    model = TestScore
    template_name = "profile/testscore_delete.html"
    success_message = "Test score deleted successfully."

    def get_queryset(self):
        assert self.request.user.is_authenticated
        owner = self.request.user
        return self.model.objects.filter(user=owner)

    def test_func(self):
        assert self.request.user.is_authenticated
        return self.request.user.can_update_profile and self.request.user.accepted_terms

    def get_success_url(self):
        return reverse("profile:index")


class DecisionCreateView(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView
):
    model = Decision
    form_class = DecisionForm
    template_name = "profile/decision_form.html"
    success_message = "Decision created successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self) -> Dict[str, Any]:
        form_kwargs = super().get_form_kwargs()
        form_kwargs["request"] = self.request
        return form_kwargs

    def test_func(self):
        assert self.request.user.is_authenticated
        return self.request.user.can_update_profile and self.request.user.accepted_terms

    def get_success_url(self):
        return reverse("profile:index")


class DecisionUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView
):
    model = Decision
    form_class = DecisionForm
    template_name = "profile/decision_form.html"
    success_message = "Decision created successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self) -> Dict[str, Any]:
        form_kwargs = super().get_form_kwargs()
        form_kwargs["request"] = self.request
        form_kwargs["edit"] = True
        return form_kwargs

    def get_queryset(self):
        assert self.request.user.is_authenticated
        owner = self.request.user
        return self.model.objects.filter(user=owner)

    def test_func(self):
        assert self.request.user.is_authenticated
        return self.request.user.can_update_profile and self.request.user.accepted_terms

    def get_success_url(self):
        return reverse("profile:index")


class DecisionDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView
):
    object: Decision
    model = Decision
    template_name = "profile/decision_delete.html"
    success_message = "Decision deleted successfully."

    def get_queryset(self):
        assert self.request.user.is_authenticated
        owner = self.request.user
        return self.model.objects.filter(user=owner)

    def test_func(self):
        assert self.request.user.is_authenticated
        return self.request.user.can_update_profile and self.request.user.accepted_terms

    def get_success_url(self):
        return reverse("profile:index")

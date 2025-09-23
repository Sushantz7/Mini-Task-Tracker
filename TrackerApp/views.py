from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View, ListView
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict

from .forms import LoginForm, RegistrationForm, TaskForm
from .models import CustomUser, Category, Task, AuditLog

from utils.helper_functions import serialize_task_obj, serialize_dict_for_audit

import json
# Create your views here.


class TrackerHomeView(TemplateView):
    template_name = "LandingPage.html"


class LoginPageView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True  # To redirect the authenticated user to the LOGIN_REDIRECT_URL defined in the settings.


class RegisterPageView(CreateView):
    template_name = "registration/register.html"
    form_class = RegistrationForm
    model = CustomUser
    success_url = reverse_lazy("login")


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "TaskTrackerPage.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pass categories for the create/edit form
        context["categories"] = Category.objects.all()

        # Build serialized tasks list (dictionaries) for the template so we have iso dates and notes etc
        tasks_qs = self.get_queryset()
        context["tasks"] = [serialize_task_obj(t) for t in tasks_qs]

        # audit logs (latest 50) for all users
        logs = AuditLog.objects.select_related("user", "task").order_by("-timestamp")[
            :50
        ]
        # prepare simple audit list for context
        context["audit_logs"] = [
            {
                "id": l.id,
                "user_email": l.user.email if l.user else "",
                "action": l.action,
                "task_name": (l.task.task_name if l.task else None),
                "timestamp": l.timestamp,
            }
            for l in logs
        ]
        return context


class TaskAjaxView(LoginRequiredMixin, View):
    """
    POST: create or update (FormData)
    DELETE: delete with JSON body {task_id}
    """

    def post(self, request, *args, **kwargs):
        task_id = request.POST.get("task_id")
        if task_id:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            # capture old data safely for audit
            old_raw = model_to_dict(task)
            old_data = serialize_dict_for_audit(old_raw)
            form = TaskForm(request.POST, instance=task)
            action = "update"
        else:
            old_data = None
            form = TaskForm(request.POST)
            action = "create"

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            # prepare task dict to return to frontend
            task_payload = serialize_task_obj(task)

            # audit log: save old and new as JSON-safe dicts
            new_raw = model_to_dict(task)
            new_data = serialize_dict_for_audit(new_raw)

            AuditLog.objects.create(
                user=request.user,
                task=task,
                action=action,
                old_value=old_data,
                new_value=new_data,
            )

            return JsonResponse({"success": True, "task": task_payload})
        else:
            # This thing returns form errors as JSON if any error occurs
            errors = {k: v for k, v in form.errors.items()}
            return JsonResponse({"success": False, "errors": errors})

    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            return HttpResponseBadRequest("Invalid JSON")

        task_id = data.get("task_id")
        if not task_id:
            return JsonResponse(
                {"success": False, "error": "task_id required"}, status=400
            )

        task = get_object_or_404(Task, id=task_id, user=request.user)
        old_raw = model_to_dict(task)
        old_data = serialize_dict_for_audit(old_raw)

        # create audit entry before deleting
        AuditLog.objects.create(
            user=request.user,
            task=task,
            action="delete",
            old_value=old_data,
            new_value=None,
        )

        task.delete()
        return JsonResponse({"success": True})

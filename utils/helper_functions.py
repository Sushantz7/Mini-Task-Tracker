from django.http import JsonResponse
from datetime import date, datetime
from TrackerApp.models import AuditLog

import json


def serialize_task_obj(task):
    """
    Return a dictionary with:
      - raw values (id, category, status code, priority code, numeric fields)
      - display values (status_display, priority_display, category_name)
      - iso dates (start_date_iso, est_end_date_iso) for <input type=date>
      - display_date_start and display_date_end for readable UI text
      - notes
      - progress (0-100 int)
    """
    # If task is a model instance:
    if hasattr(task, "id"):
        t = task
        category_id = t.category.id if t.category else None
        category_name = t.category.name if t.category else ""
        status = t.status
        priority = t.priority
        numeric_target = t.numeric_target
        numeric_current = t.numeric_current
        start_date = t.start_date
        est_end_date = t.est_end_date
        notes = t.notes or ""
        task_id = t.id
        task_name = t.task_name
    # If task is a dict (already model_to_dict):
    else:
        d = task
        task_id = d.get("id")
        task_name = d.get("task_name")
        category_id = d.get("category")
        category_name = d.get("category_name", "")
        status = d.get("status")
        priority = d.get("priority")
        numeric_target = d.get("numeric_target")
        numeric_current = d.get("numeric_current")
        start_date = d.get("start_date")
        est_end_date = d.get("est_end_date")
        notes = d.get("notes", "")

    # safe iso formatting
    def iso(v):
        if isinstance(v, (date, datetime)):
            return v.isoformat()
        return v or ""

    # display date (YYYY-MM-DD)
    start_iso = iso(start_date)
    end_iso = iso(est_end_date)

    # if we have iso strings use them, else blank
    start_display = start_iso[:10] if start_iso else ""
    end_display = end_iso[:10] if end_iso else ""

    try:
        pct = int(
            round((float(numeric_current or 0) / float(numeric_target or 1)) * 100)
        )
        if pct < 0:
            pct = 0
        if pct > 100:
            pct = 100
    except Exception:
        pct = 0

    # human labels
    try:
        status_display = (
            t.get_status_display()
            if "t" in locals()
            else {"todo": "To Do", "in_progress": "In Progress", "done": "Done"}.get(
                status, status
            )
        )
    except Exception:
        status_display = {
            "todo": "To Do",
            "in_progress": "In Progress",
            "done": "Done",
        }.get(status, status)

    try:
        priority_display = (
            t.get_priority_display()
            if "t" in locals()
            else {"high": "High", "medium": "Medium", "low": "Low"}.get(
                priority, priority
            )
        )
    except Exception:
        priority_display = {"high": "High", "medium": "Medium", "low": "Low"}.get(
            priority, priority
        )

    return {
        "id": task_id,
        "task_name": task_name,
        "category": category_id,
        "category_name": category_name,
        "status": status,
        "status_display": status_display,
        "priority": priority,
        "priority_display": priority_display,
        "numeric_target": numeric_target,
        "numeric_current": numeric_current,
        "start_date_iso": start_iso,
        "est_end_date_iso": end_iso,
        "start_date_display": start_display,
        "est_end_date_display": end_display,
        "notes": notes,
        "progress": pct,
    }


# Helper to serialize dicts (old/new values) for AuditLog
def serialize_dict_for_audit(d):
    """Given a dict (from model_to_dict), convert date/datetime to iso strings."""
    safe = {}
    for k, v in (d or {}).items():
        if isinstance(v, (date, datetime)):
            safe[k] = v.isoformat()
        else:
            # if value is a model instance or other complex object we str it.
            try:
                json.dumps(v)
                safe[k] = v
            except Exception:
                safe[k] = str(v)
    return safe


# Audit detail endpoint (returns old/new data for a single audit log)
def audit_detail(request, pk):
    """
    Returns JSON with old_value and new_value for an AuditLog record.
    This is a simple view (no template) used by JS when clicking a log entry.
    """
    try:
        log = AuditLog.objects.get(pk=pk)
    except AuditLog.DoesNotExist:
        return JsonResponse({"success": False, "error": "not found"}, status=404)

    # This is a helper function that is used to convert old/new dict values into strings
    def format_values(val):
        if not val:
            return None
        filtered = {
            k: str(v) for k, v in val.items() if k not in ("id", "user_id", "user")
        }
        return filtered

    return JsonResponse(
        {
            "success": True,
            "user_email": log.user.email if log.user else "Unknown",
            "action": log.get_action_display(),
            "task_name": log.task.task_name if log.task else "N/A",
            "timestamp": log.timestamp.strftime("%b %d, %Y %H:%M"),
            "old_value": format_values(log.old_value),
            "new_value": format_values(log.new_value),
        }
    )

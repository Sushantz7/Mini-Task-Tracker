from django import template

register = template.Library()


@register.filter
def status_color(status):
    colors = {
        "To Do": "gray",
        "In Progress": "blue",
        "Done": "green",
    }
    return colors.get(status, "gray")


@register.filter
def priority_color(priority):
    colors = {
        "High": "red",
        "Medium": "yellow",
        "Low": "green",
    }
    return colors.get(priority, "gray")

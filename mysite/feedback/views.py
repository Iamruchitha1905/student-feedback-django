from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.db.models import Avg, Count
from django.contrib import messages
from .models import Feedback
import csv


# ----------------------
# Public Pages
# ----------------------

def home(request):
    return render(request, "home.html")


def submit_feedback(request):
    if request.method == "POST":
        Feedback.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            course=request.POST["course"],
            rating=request.POST["rating"],
            comments=request.POST["comments"]
        )
        return redirect("thankyou")
    
    return render(request, "submit.html")


def thankyou(request):
    return render(request, "thankyou.html")


# ----------------------
# Authentication
# ----------------------

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! Please log in.")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


# ----------------------
# Protected Pages
# ----------------------

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-submitted_at')
    return render(request, "list.html", {"feedbacks": feedbacks})


@login_required
def dashboard(request):
    # Basic statistics
    total = Feedback.objects.count()
    avg_rating = Feedback.objects.aggregate(Avg('rating'))["rating__avg"]

    # Feedback per course
    course_stats = (
        Feedback.objects.values('course')
        .annotate(count=Count('course'))
        .order_by('course')
    )

    # Latest feedback
    latest_feedback = Feedback.objects.order_by('-submitted_at')[:5]

    # Chart data
    chart_labels = [c['course'] for c in course_stats]
    chart_values = [c['count'] for c in course_stats]

    return render(request, "dashboard.html", {
        "total": total,
        "avg_rating": avg_rating,
        "course_stats": course_stats,
        "latest_feedback": latest_feedback,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
    })


# ----------------------
# CSV Export
# ----------------------

@login_required
def export_csv(request):
    """Export feedback data to CSV."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=feedback.csv"

    writer = csv.writer(response)
    writer.writerow(["Name", "Email", "Course", "Rating", "Comments", "Submitted At"])

    for f in Feedback.objects.all():
        writer.writerow([
            f.name,
            f.email,
            f.course,
            f.rating,
            f.comments,
            f.submitted_at
        ])

    return response
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import QuestionForm
from .models import QAEntry


def home(request):
    return render(request, "home.html")


def register_user(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():

            return render(
                request,
                "register.html",
                {
                    "error": "Username already exists"
                }
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("login")

    return render(request, "register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def ask_question(request):

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():

            question = form.cleaned_data["question"]

            QAEntry.objects.create(
                user=request.user,
                question_text=question,
                answer_text="Pending",
                plugin_source="Manual"
            )

            return render(
                request,
                "ask_question.html",
                {
                    "form": QuestionForm(),
                    "success": True
                }
            )

    else:
        form = QuestionForm()

    return render(
        request,
        "ask_question.html",
        {
            "form": form
        }
    )


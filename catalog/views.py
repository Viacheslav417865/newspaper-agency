from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from catalog.form import (
    NewspaperForm,
    RedactorCreationForm,
    RedactorUpdateForm,
    TopicSearchForm,
    RedactorSearchForm,
    NewspaperSearchForm,
    LoginForm,
)
from catalog.models import Redactor, Topic, Newspaper
from .base_views import BaseView


class LoginView(BaseView):
    def get(self, request):
        form = LoginForm()
        return self.render_view(request,
                                "registration/login.html",
                                {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get("next", "/")
                return redirect(next_url)
            else:
                msg = "Invalid credentials"
                return self.render_view(request,
                                        "registration/login.html",
                                        {"form": form, "msg": msg})


class LogoutView(BaseView):
    def get(self, request):
        logout(request)
        next_url = request.GET.get("next", "/")
        return redirect("login")

    def post(self, request):
        logout(request)
        return redirect("login")

class IndexView(BaseView):
    def get(self, request):
        redactor = Redactor.objects.all()
        newspaper = Newspaper.objects.all()
        num_redactors = redactor.count()
        num_topics = Topic.objects.count()
        num_newspapers = newspaper.count()

        num_visits = request.session.get("num_visits", 0)
        request.session["num_visits"] = num_visits + 1

        context = {
            "redactor_info": redactor.order_by("-years_of_experience")[:5],
            "newspaper_articles": newspaper.order_by("-published_date")[:5],
            "num_redactors": num_redactors,
            "num_topics": num_topics,
            "num_newspapers": num_newspapers,
            "num_visits": num_visits + 1,
        }
        return self.render_view(request, "catalog/index.html", context)


class TopicListView(BaseView, ListView):
    model = Topic
    paginate_by = 5
    queryset = Topic.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["topic_list"] = self.object_list
        context["search_form"] = TopicSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TopicSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class TopicCreateView(BaseView, CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("catalog:topic-list")


class TopicUpdateView(BaseView, UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("catalog:topic-list")


class TopicDetailView(BaseView, DetailView):
    model = Topic
    template_name = "catalog/topic_detail.html"


class TopicDeleteView(BaseView, DeleteView):
    model = Topic
    success_url = reverse_lazy("catalog:topic-list")


class NewspaperListView(BaseView, ListView):
    model = Newspaper
    paginate_by = 5
    queryset = Newspaper.objects.select_related("topic")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = (
            NewspaperSearchForm(initial={"title": title}))
        context["newspaper_list"] = self.object_list
        return context

    def get_queryset(self):
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return self.queryset


class NewspaperDetailView(BaseView, DetailView):
    model = Newspaper


class NewspaperCreateView(BaseView, CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("catalog:newspaper-list")

    def get_success_url(self):
        return reverse_lazy("catalog:newspaper-detail",
                            kwargs={'pk': self.object.pk})


class NewspaperUpdateView(BaseView, UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("catalog:newspaper-list")


class NewspaperDeleteView(BaseView, DeleteView):
    model = Newspaper
    success_url = reverse_lazy("catalog:newspaper-list")


class RedactorListView(BaseView, ListView):
    model = Redactor
    paginate_by = 5
    queryset = Redactor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(initial={"username": username})
        context["redactor_list"] = self.object_list
        return context

    def get_queryset(self):
        form = RedactorSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(username__icontains=form.cleaned_data["username"])
        return self.queryset


class RedactorDetailView(DetailView):
    model = Redactor
    template_name = "catalog/redactor_detail.html"
    context_object_name = "redactor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "redactor" in context:
            print(context["redactor"].id)
        return context


class RedactorCreationView(BaseView, CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("catalog:redactor-list")


class RedactorUpdateView(BaseView, UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm
    success_url = reverse_lazy("catalog:redactor-list")


class RedactorDeleteView(BaseView, DeleteView):
    model = Redactor
    success_url = reverse_lazy("catalog:redactor-delete")


@login_required
def toggle_assign_to_newspaper(request, pk):
    redactor = Redactor.objects.get(id=request.user.id)
    if Newspaper.objects.get(id=pk) in redactor.newspaper.all():
        redactor.newspaper.remove(pk)
    else:
        redactor.newspaper.add(pk)
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect(
        reverse_lazy("catalog:newspaper-detail", args=[pk])
    )

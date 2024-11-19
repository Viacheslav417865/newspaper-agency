from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class BaseView(LoginRequiredMixin, View):
    @staticmethod
    def render_view(request, template_name,
                    context=None):
        if context is None:
            context = {}
        return render(request, template_name, context)

    def handle_form_submission(self, form, request, success_url):
        if form.is_valid():
            form.save()
            return redirect(success_url)
        else:
            return self.render_view(request,
                                    "redactor_form.html",
                                    {"form": form})

    def get_context_data(self, **kwargs):
        return kwargs

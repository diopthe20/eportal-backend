from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.views.generic.edit import FormView

from agent.pdf.models import PDFAgent

from .forms import FileFieldForm
from .tasks import run_batch


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "agent/upload.html"
    success_url = "agent/success.html"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            pdf = PDFAgent.objects.create(pdf_cv_file=f)
            pdf.save()

            print(pdf.id)
            run_batch.delay(pdf.id)
        return super().form_valid(form)


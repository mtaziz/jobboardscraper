from django.conf import settings
from django.views.generic import DetailView, ListView

from jobs.models import Job


class JobDetailView(DetailView):
    model = Job

job_detail = JobDetailView.as_view()


class JobListView(ListView):
    model = Job
    paginate_by = getattr(settings, 'PAGINATE_BY', 10)

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['job_count'] = Job.objects.count()
        return context

job_list = JobListView.as_view()

'''Views for the ethernet authentication application.'''
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views import generic

from .forms import SwitchPortActionForm
from .models import SwitchPort
from .models import SwitchPortAction


class SwitchPortView(LoginRequiredMixin, generic.ListView):
    template_name = 'ethernet_auth/switchPorts.html'
    context_object_name = 'switch_ports_list'

    def get_queryset(self):
        return SwitchPort.objects.all()


class SwitchPortDetailView(LoginRequiredMixin, generic.DetailView):
    model = SwitchPort


class SwitchPortActionCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = SwitchPortActionForm
    model = SwitchPortAction
    success_url = reverse_lazy('ethernet_auth:switch_port_list')

    def form_valid(self, form):
        action = form.save(commit=False)
        action.user = self.request.user
        action.switch_port = get_object_or_404(SwitchPort, pk=self.kwargs['pk'])

        try:
            action.full_clean()
        except ValidationError as e:
            form.add_error(None, str(e))
            return super(SwitchPortActionCreateView, self).form_invalid(form)

        messages.success(self.request, 'Action enregistrée avec succès.')
        return super(SwitchPortActionCreateView, self).form_valid(form)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views import generic

from ..forms.interface import InterfaceForm
from ..models.device import Device
from ..models.interface import Interface


def get_interface(kwargs, request, queryset=None):
    device = get_object_or_404(
        Device,
        pk=kwargs['pk1'],
        user=request.user,
    )

    return get_object_or_404(
        Interface,
        pk=kwargs['pk2'],
        device=device,
    )


# Views for the interface model

class InterfaceCreateView(generic.edit.CreateView):
    '''Add the device referenced in url as the interface owner.'''

    model = Interface
    form_class = InterfaceForm

    def form_valid(self, form):
        interface = form.save(commit=False)
        device = get_object_or_404(
            Device,
            pk=self.kwargs['pk'],
            user=self.request.user,
        )

        interface.device = device
        interface.full_clean()

        return super(InterfaceCreateView, self).form_valid(form)


class InterfaceUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    success_url = reverse_lazy('network:index')
    form_class = InterfaceForm

    def get_object(self, queryset=None):
        return get_interface(self.kwargs, self.request, queryset=None)


class InterfaceDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    success_url = reverse_lazy('network:index')
    model = Interface

    def get_object(self, queryset=None):
        return get_interface(self.kwargs, self.request, queryset=None)

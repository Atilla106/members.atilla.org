from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django import forms

from ..models import Device, Interface, INTERFACE_TYPE_CHOICES


def get_interface(kwargs, request, queryset=None):
    device = get_object_or_404(Device,
                               pk=kwargs['pk1'],
                               user=request.user)
    return get_object_or_404(Interface,
                             pk=kwargs['pk2'],
                             device=device)


""" Form declaration for the interface model """


class InterfaceForm(forms.ModelForm):
    interface_type = forms.ChoiceField(choices=INTERFACE_TYPE_CHOICES)
    mac_address = forms.CharField()
    description = forms.CharField()

    class Meta:
        model = Interface
        fields = ['interface_type', 'mac_address', 'description']


""" Views for the interface model """


class InterfaceCreateView(generic.edit.CreateView):
    model = Interface
    form_class = InterfaceForm

    """ Add the device referenced in url as the interface owner """
    def form_valid(self, form):
        interface = form.save(commit=False)
        device = get_object_or_404(Device,
                                   pk=self.kwargs['pk'],
                                   user=self.request.user)
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

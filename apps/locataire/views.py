from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView
from web_project import TemplateLayout
from django.shortcuts import render, redirect
from .models import Locataire, TypePersonne
from .forms import LocataireForm

# Create your views here.
class LocataireView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["locataires"] = Locataire.objects.all()
        context["form"] = LocataireForm()
        return context

    def post(self, request, *args, **kwargs):
        form = LocataireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('locataire-list')
        else:
            context = self.get_context_data()
            context["form"] = form
            return self.render_to_response(context)
            #return render(request, 'locataire/locataire.html', {'form': form})

#class LocataireCreateView(FormView):
#    model = Locataire
#    form_class = LocataireForm
#    success_url = '/locataire/list/'
#
#    def form_valid(self, form):
#        return super().form_valid(form)
    

#def locataire_new(request):
#    if request.method == "POST":
#        form = LocataireForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('locataire_list')
#    else:
#        form = LocataireForm()
#    return render(request, 'locataire/locataire.html', {'form': form})
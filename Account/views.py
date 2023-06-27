from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ProfileForm,EducationForm
from django.views.generic import UpdateView,TemplateView,View
from .models import Profile,ProfileCV
from django.shortcuts import get_object_or_404
from django.forms import formset_factory

# from 

# Create your views here.


class UserProfile(TemplateView):
    template_name = "profiles/user-profile.html"
    
    def get_context_data(self, slug,**kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile.objects.select_related('user'),slug=slug)
        jobs = profile.user.job_set.count()
        applications = profile.user.user_application.count()
        successful_applications = profile.user.user_application.filter(status="AcceptJob").count()
        
        context= {'jobs':jobs,'applications':applications,'successful_applications':successful_applications,'profile':profile}
        return context
    

class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = "profiles/update-profile.html"
    form_class = ProfileForm
    
    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        documents = self.request.FILES.getlist('documents')
        for document in documents:
            ProfileCV.objects.create(profile=profile, user= self.request.user,cv=document)
        
        return super(ProfileUpdateView,self).form_valid(form)
class EditEducationView(View):
    
    EducationFormSet = formset_factory(EducationForm,extra=1)
    template_name = "profiles/user-profile.html"
    
    
    
    
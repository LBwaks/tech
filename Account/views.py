from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import ProfileForm,EducationForm
from django.views.generic import UpdateView,TemplateView,View
from .models import Profile,ProfileCV,Education
from django.shortcuts import get_object_or_404


# from 

# Create your views here.


class UserProfile(TemplateView):
    template_name = "profiles/user-profile.html"
    
    
    def get_context_data(self, slug,**kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile.objects.select_related('user'),slug=slug)
        educations= Education.objects.filter(user_profile_id=profile.id)
        jobs = profile.user.job_set.count()
        applications = profile.user.user_application.count()
        successful_applications = profile.user.user_application.filter(status="AcceptJob").count()
        form = EducationForm()
       
        context= {'jobs':jobs,'applications':applications, 'educations':educations,'form':form, 'successful_applications':successful_applications,'profile':profile}
        return context
    
    def post(self,request,slug,**kwargs):
        profile= get_object_or_404(Profile,slug=slug)
        if request.method == "POST":
            form = EducationForm(request.POST)
            if form.is_valid():
                    
                education = form.save(commit=False)
                education.user_profile_id = profile.id
                education.save()
                        
                return HttpResponseRedirect(request.META["HTTP_REFERER"])
            else :
                context = self.get_context_data(slug=slug)
                context['form']= form
        return self.render_to_response(context)
    
def deleteEducation(request,slug):
    education =get_object_or_404(Education,slug=slug)
    if education:
        education.delete()
    return  HttpResponseRedirect(request.META["HTTP_REFERER"])

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
# class EditEducationView(View):
    
#     EducationFormSet = formset_factory(EducationForm)  
#     template_name = "profiles/user-profile.html"
    
#     def get(self,request):
#         formset = self.EducationFormSet()
#         return render(request,self.template_name,{formset:formset})
    
#     def post(self,request):
#         formset = self.EducationFormSet(request.POST)
#         if formset.is_valid():
#             for  form in formset:
#                 form.save()
#             return HttpResponseRedirect(request.META["HTTP_REFERER"])
#         return render(request,self.template_name,{formset:formset})

def addEducation(request):
    EducationFormSet= formset_factory(EducationForm) 
    ddu = EducationFormSet()
    for form in ddu:
        print("hey there")
        print(form.as_table())
    if request.method == "POST":
        formset = EducationFormSet(request.POST)
        # if formset.is_valid():
        #     for form in formset:
        #         form.save()
            # return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        formset = EducationFormSet()
    return render (request,"profiles/update-profile.html",{"formset":formset})
    
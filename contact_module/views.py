from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView
from site_module.models import SiteSetting
from .forms import ContactUsModelForm
from .models import ContactUs, UserProfile


class ContactUsView(CreateView):
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact_us_page.html'
    success_url = "/contact_us"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting
        return context


def store_file(file):
    with open('temp/image.jpg', "wb+") as dest:
        for chunk in file.chunks():
            dest.write(chunk)


class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact_us/create_profile'


class ProfilesView(ListView):
    model = UserProfile
    template_name = 'contact_module/profile_list_page.html'
    context_object_name = "profiles"

# ------------------------different types of this shit --------------------------------------

# class CreateProfileView(View):
#     def get(self, request):
#         form = ProfileForm()
#         return render(request, 'contact_module/create_profile_page.html', {
#             'form': form
#         })
#
#     def post(self, request):
#         submitted_form = ProfileForm(request.POST, request.FILES)
#
#         if submitted_form.is_valid():
#             # store_file(request.FILES['profile'])
#             profile = UserProfile(image=request.FILES['user_image'])
#             profile.save()
#             print("a")
#             return redirect("/contact_us")
#
#         return render(request, 'contact_module/create_profile_page.html', {
#             'form': submitted_form
#         })
# class ContactUsView(FormView):
#     template_name = 'contact_module/contact_us_page.html'
#     form_class = ContactUsModelForm
#     success_url = "/contact_us"
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

# class ContactUsView(View):
#     def get(self, request):
#         contact_form = ContactUsModelForm()
#         return render(request, 'contact_module/contact_us_page.html', {
#             "contact_form": contact_form
#         })
#
#     def post(self, request):
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             return redirect('home_page')
#
#         return render(request, 'contact_module/contact_us_page.html', {
#             "contact_form": contact_form
#         })


# def contact_us(request):
#     if request.method == 'POST':
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             return redirect('home_page')
#
#     else:
#         contact_form = ContactUsModelForm()
#
#     return render(request, 'contact_module/contact_us_page.html', {
#         "contact_form": contact_form
#     })

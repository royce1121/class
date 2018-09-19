from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Person, Person1
from .forms import AddForm
from .resources import PersonResource
from django.http import HttpResponse
from django.views.generic import View
from tablib import Dataset
from django.views.generic import ListView, FormView, TemplateView

# Create your views here.
# user


class Home(ListView):
    model = Person
    context_object_name = 'contact'
    queryset = Person.objects.all()
    template_name = 'finalexam/home.html'


class qwerty(TemplateView):
    template_name = 'finalexam/signup.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        username = request.POST['user']
        password = request.POST['pass']
        email = request.POST['mail']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
            return render(request, 'finalexam/home.html', {})


class LoginView(View):
    template_name = 'finalexam/home.html'

    def post(self, request):
        username = request.POST['user']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)

        if user:
            auth_login(request, user)
            contact = Person.objects.filter(author=username)
            return render(request, self.template_name, {'contact': contact})
        else:
            return render(request, self.template_name, {'error_message': "Invalid email or password! Please try again."})


class LogoutView(View):
    template_name = 'finalexam/home.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name, {})


class Add(FormView):
    template_name = 'finalexam/add.html'
    form_class = AddForm

    def get(self, request):
        form = self.get_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.user.username
        form = self.get_form()
        if form.is_valid():
            fname = form['fname'].value()
            lname = form['lname'].value()
            contact = form['contact'].value()
            address = form['address'].value()
            check = Person.objects.filter(
                First_name=fname,
                Last_name=lname,
                author=username)
            if check.exists():
                contact = Person.objects.filter(author=username)
                return render(request, 'finalexam/home.html', {'contact': contact, 'error_message': "Error, This data is already existing"})
            else:
                new = Person.objects.create(
                    First_name=fname,
                    Last_name=lname,
                    contact=contact,
                    address=address,
                    author=username)
                new.save()
                contact = Person.objects.filter(author=username)
                return render(request, 'finalexam/home.html', {'contact': contact})


# def add(request):
#     if not request.user.is_authenticated:
#         return render(request, 'finalexam/home.html', {'error_message': "Please Login to access this page"})
#     else:
#         if request.POST:
#             form = AddForm()
#             return render(request, 'finalexam/add.html', {'form': form})

# def add1(request):
#   if not request.user.is_authenticated:
#       return render(request, 'finalexam/home.html', {'error_message':"Please Login to access this page"})
#   else:
#       if request.method == 'POST':
#           username = request.user.username
#           form = AddForm(request.POST)
#           if form.is_valid():
#               fname = form['fname'].value()
#               lname = form['lname'].value()
#               contact = form['contact'].value()
#               address = form['address'].value()
#               check = Person.objects.filter(First_name=fname, Last_name=lname, author=username)
#               if check.exists():
#                   contact = Person.objects.filter(author=username)
#                   return render(request, 'finalexam/home.html', {'contact': contact, 'error_message': "Error, This data is already existing"})
#               else:
#                   new = Person.objects.create(First_name=fname, Last_name=lname, contact=contact, address=address, author=username)
#                   new.save()
#                   contact = Person.objects.filter(author=username)
#                   return render(request, 'finalexam/home.html', {'contact': contact})
class Remove(ListView):

    def get(self, request, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            rem = get_object_or_404(Person, pk=pk)
            rem = Person.objects.filter(pk=pk)
            return render(request, 'finalexam/remove.html', {'rem': rem})

        except:
            username = request.user.username
            contact = Person.objects.filter(author=username)
            return render(request, 'finalexam/home.html', {
                'contact': contact,
                'error_message': "Error, Object missing or already deleted."})


class Remove1(ListView):

    template_name = 'finalexam/home.html'

    def get_context_data(self, **kwargs):
        context = super(Remove1, self).get_context_data(**kwargs)
        context.update({
            'rem': self.get_queryset(),
        })
        return context

    def get_queryset(self):
        username = self.request.user.username
        print (Person.objects.filter(author=username))
        return Person.objects.filter(author=username)

    def get(self, request, *args, **kwargs):
        username = request.user.username
        try:
            pk = self.kwargs['pk']
            rem = get_object_or_404(Person, pk=pk)
            rem.delete()
            contact = Person.objects.filter(author=username)
            return render(request, self.template_name, {
                'contact': contact})
        except:
            contact = Person.objects.filter(author=username)
            return render(request, self.template_name, {
                'contact': contact,
                'error_message': "Error, Object missing or already deleted."})
# def remove1(request, pk):
#   if not request.user.is_authenticated:
#       return render(request, 'finalexam/home.html', {'error_message': "Please Login to access this page"})
#   else:
#       username = request.user.username
#       try:
#           rem = get_object_or_404(Person, pk=pk)
#           rem.delete()
#           contact = Person.objects.filter(author=username)
#           return render(request, 'finalexam/home.html', {'contact': contact})
#       except:
#           contact = Person.objects.filter(author=username)
#           return render(request, 'finalexam/home.html', {'contact': contact, 'error_message':"Error, Object missing or already deleted."})
# edit


class Edit(FormView, ListView):
    form_class = AddForm

    def get(self, request, *args, **kwargs):
        # try:
            pk = self.kwargs['pk']
            form = self.get_form()
            edit1 = get_object_or_404(Person, pk=pk)
            return render(request, 'finalexam/edit.html', {
                'edit1': edit1,
                'form': form})
        # except:
        #     sect = Person.objects.all()
        #     form = self.get_form()
        #     return render(request, 'finalexam/home.html', {
        #         'sect': sect,
        #         'error_message': 'Error, object missing or already deleted.'})

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            username = request.user.username
            edit1 = get_object_or_404(Person, pk=pk)
            if request.method == 'POST':
                form = self.get_form()
                if form.is_valid():
                    fname = form['fname'].value()
                    lname = form['lname'].value()
                    contact = form['contact'].value()
                    address = form['address'].value()
                    check = Person.objects.filter(
                        First_name=fname,
                        Last_name=lname)
                    if check.exists():
                        contact = Person.objects.filter(author=username)
                        return render(request, 'finalexam/home.html', {
                            'contact': contact,
                            'error_message': "Error, Data Already Exist"})
                    else:
                        Person.objects.filter(
                            First_name=edit1.First_name,
                            Last_name=edit1.Last_name).update(
                            First_name=fname,
                            Last_name=lname,
                            contact=contact,
                            address=address)
                        contact = Person.objects.filter(author=username)
                        return render(request, 'finalexam/home.html', {'contact': contact})
        except:
            contact = Person.objects.filter(author=username)
            return render(request, 'finalexam/home.html', {
                'contact': contact,
                'error_message': "Error, Object missing or already deleted."})
# def edit(request, pk):
#   if not request.user.is_authenticated:
#       return render(request, 'finalexam/home.html', {'error_message':"Please Login to access this page"})
#   else:
#       form = AddForm()
#       try:
#           edit1 = get_object_or_404(Person, pk=pk)
#           return render(request, 'finalexam/edit.html', {'edit1': edit1,'form': form})
#       except:
#           sect = Person.objects.all()
#           form = AddForm()
#           return render(request, 'finalexam/home.html', {'sect': sect, 'error_message':"Error, Object missing or already deleted."})


# def edit1(request, pk):
#     if not request.user.is_authenticated:
#         return render(request, 'finalexam/home.html', {'error_message': "Please Login to access this page"})
#     else:
#         try:
#             username = request.user.username
#             edit1 = get_object_or_404(Person, pk=pk)
#             if request.method == 'POST':
#                 form = AddForm(request.POST)
#                 if form.is_valid():
#                     fname = form['fname'].value()
#                     lname = form['lname'].value()
#                     contact = form['contact'].value()
#                     address = form['address'].value()
#                     check = Person.objects.filter(First_name=fname, Last_name=lname)
#                     if check.exists():
#                         contact = Person.objects.filter(author=username)
#                         return render(request, 'finalexam/home.html', {'contact': contact, 'error_message': "Error, Data Already Exist"})
#                     else:
#                         Person.objects.filter(
#                             First_name=edit1.First_name,
#                             Last_name=edit1.Last_name).update(
#                             First_name=fname,
#                             Last_name=lname,
#                             contact=contact,
#                             address=address)
#                         contact = Person.objects.filter(author=username)
#                         return render(request, 'finalexam/home.html', {'contact': contact})
#         except:
#             contact = Person.objects.filter(author=username)
#             return render(request, 'finalexam/home.html', {'contact': contact, 'error_message': "Error, Object missing or already deleted."})

class export(View):

    def get(self, request):
        username = request.user.username
        contact = Person.objects.filter(author=username)
        for contact in contact:
            Person1.objects.create(First_name=contact.First_name, Last_name=contact.Last_name, contact=contact.contact, address=contact.address)
        person_resource = PersonResource()
        queryset = Person.objects.filter(author=username)
        dataset = person_resource.export(queryset)
        Person1.objects.all().delete()
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="list.csv"'
        return response


class import1(TemplateView):
    template_name = 'finalexam/import.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        person_resource = PersonResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']
        username = request.user.username

        imported_data = dataset.load(new_persons.read().decode('utf-8'), format='csv')
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now
            contact = Person1.objects.filter()
            for contact in contact:
                Person.objects.create(
                    First_name=contact.First_name,
                    Last_name=contact.Last_name,
                    contact=contact.contact,
                    address=contact.address,
                    author=username)
            Person1.objects.all().delete()
        contact = Person.objects.filter(author=username)
        return render(request, 'finalexam/home.html', {'contact': contact})

# def simple_upload(request):
#     if request.method == 'POST':
#         person_resource = PersonResource()
#         dataset = Dataset()
#         new_persons = request.FILES['myfile']
#         username = request.user.username

#         imported_data = dataset.load(new_persons.read().decode('utf-8'), format='csv')
#         result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

#         if not result.has_errors():
#             person_resource.import_data(dataset, dry_run=False)  # Actually import now
#             contact = Person1.objects.filter()
#             for contact in contact:
#                 Person.objects.create(
#                     First_name=contact.First_name,
#                     Last_name=contact.Last_name,
#                     contact=contact.contact,
#                     address=contact.address,
#                     author=username)
#             Person1.objects.all().delete()
#     contact = Person.objects.filter(author=username)
#     return render(request, 'finalexam/home.html', {'contact': contact})

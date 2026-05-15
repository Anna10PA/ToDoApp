from django.shortcuts import render, redirect
from .forms import regForm, logForm
from .models import registration

# მთავარი გვერდი
def home(req):
    return render(req, 'index.html')

# შესვლა
def loginForm(req):
    if req.method == 'POST':
        form = logForm(req.POST)
        users = registration.objects.all().values()

        if form.is_valid():
            user = list(filter(lambda u: (u['email'] == form.cleaned_data.get('username_or_email') or u['username'] == form.cleaned_data.get('username_or_email')) and u['password'] == form.cleaned_data.get('password'), users))
            if len(user) > 0:
                req.session['user'] = user[0]
                return redirect('main_page')
    return render(req, 'login.html', {'form': logForm()})

# რეგისტრაცია
def registrationForm(req):
    if req.method == 'POST':
        form = regForm(req.POST)
        users = registration.objects.all().values()

        if form.is_valid():
            user = list(filter(lambda u: u['email'] == form.cleaned_data.get('email') or u['username'] == form.cleaned_data.get('username'), users))
            if len(user) > 0:
                return render(req, 'registration.html', {'form': regForm(), 'error': 'This email or username already exists'})
            else:
                form.save()
                return render(req, 'registration.html', {'message': 'Registration completed successfully'})
        return render(req, 'index.html')
    return render(req, 'registration.html', {'form': regForm()})

# მომხმარებლის გვერდი
def main_p(req):
    return render(req, 'main.html', {
        'username': req.session['user'].get('username'),
        'name': req.session['user'].get('name')
    })

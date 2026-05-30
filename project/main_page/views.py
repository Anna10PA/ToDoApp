from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import regForm, logForm
from .models import registration
import uuid

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

# მეილზე კოდის გაგზავნა
def email(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        user = list(filter(lambda u: u.get('email') == email, list(registration.objects.all().values())))

        if user:
            code = str(uuid.uuid4()).split('-')[0]
            try:
                req.session['code'] = code
                req.session['email'] = email
                send_mail('ToDoApp.co', f'this is code {code}', settings.EMAIL_HOST_USER, [email])
                return redirect('code')

            except Exception as error:
                return render(req, 'email.html', {'message': error})

        else:
            return render(req, 'email.html', {'message': 'email is not found'})
    
    return render(req, 'email.html')

# კოდის შეყვანა
def code(req):
    code = req.session.get('code')

    if code:
        if req.method == 'POST':
            user_code = req.POST.get('code')
            if code == user_code:
                return redirect('password')
            else:
                return render(req, 'code.html', {'message': 'code is not correct'})

    return render(req, 'code.html')

# პაროლის შეცვლა
def password(req):
    if req.method == 'POST':
        email = req.session.get('email')
        if email:
            user = registration.objects.get(email=email)
            new_password = req.POST.get('password')

            if len(new_password) < 8 and new_password == user.get('username') and (new_password.lower() == new_password or new_password == new_password.upper()):
                return render(req, 'password.html', {'message': 'this password is not recomended'})
            else:
                user.password = new_password
                user.save()
                return redirect('login')

    return render(req, 'password.html')

# მომხმარებლის გვერდი
def main_p(req):
    return render(req, 'main.html', {
        'username': req.session['user'].get('username'),
        'name': req.session['user'].get('name')
    })

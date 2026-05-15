from django.shortcuts import render, redirect

# მომხმარებლის საწყისი გვერდი
def main(req):
    return render(req, 'main.html')

# მომხმარებლის პროფილის ნახვა
def profile(req):
    if 'user' not in req.session:
        return redirect('login')
    
    return render(req, 'profile.html', {
        'user': req.session['user']
    })

# დავალებების გვერდი
def task(req):
    return render(req, 'tasks.html')
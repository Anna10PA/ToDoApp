from django.shortcuts import render, redirect
from .forms import taskForm
from .models import task, delt
from datetime import datetime

# მთავარი გვერდი
def tasks(req):
    return render(req, 'tasks.html')

# დავალების დამატება
def add_new_task(req):
    if req.method == 'POST':
        task_model = taskForm(req.POST)

        if task_model.is_valid():
            item = task_model.save(commit=False)
            item.email = req.session['user'].get('email')
            item.save()

    return redirect('tasks')

# ყველა დავალების ნახვა
def all_tasks(req):
    user_tsk = list(filter(lambda u: u['email'] == req.session['user'].get('email'), list(task.objects.all().values())))
    return render(req, 'all_task.html', {'tasks': user_tsk})

# წაშლა დავალებებიდან
def delete(req, id):
    if req.session['user']:
        user_tsk = task.objects.get(id=id)

        add_dlt = delt(id=id, tasks=user_tsk.tasks, add_time=user_tsk.add_time, email=user_tsk.email, completed_time=user_tsk.completed_time, deadline_time=user_tsk.deadline_time)
        add_dlt.save()
        
        user_tsk.delete()        
        return redirect('all')

# წაშლილები 
def del_page(req):
    return render(req, 'delete.html', {
        'tasks': list(filter(lambda u: u['email'] == req.session['user'].get('email'), list(delt.objects.all().values().order_by('deleted_time'))))
        })

# წაშლილებიდან ყველას წაშლა
def delete_all(req):
    if req.session.get('user'):
        delt.objects.all().delete()
    return redirect('del_page')

# წაშლილებიდან ერთ-ერთის წაშლა
def delete_from_delete(req, id):
    if req.session.get('user'):
        delt.objects.get(id=id).delete()
    return redirect('del_page')

# შესრულებულში დამატება
def completed(req, id):
    if req.session.get('user') and req.method == 'POST':
        comp_tsk = task.objects.all().get(id=id, email=req.session['user'].get('email'))

        if not comp_tsk.completed_time:
            comp_tsk.completed_time = datetime.now()
        else:
            comp_tsk.completed_time = None
        comp_tsk.save()
    return redirect('all')

# წაშლილებიდან დაბრუნება
def return_from_delete(req, id):
    if req.session.get('user'):
        tsk = delt.objects.all().get(id=id, email=req.session['user'].get('email'))
        all_tsk = task(id=id, tasks=tsk.tasks, add_time=tsk.add_time, email=tsk.email, completed_time=tsk.completed_time, deadline_time=tsk.deadline_time, deleted_time = None)

        all_tsk.save()
        tsk.delete()

    return redirect('del_page')
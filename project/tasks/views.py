from django.shortcuts import render, redirect
from .forms import taskForm
from .models import task, delt, category
from datetime import datetime

# მთავარი გვერდი
def tasks(req):
    if req.session.get('user'):
        return render(req, 'tasks.html', {'category': list(filter(lambda ctg: ctg.get('email') == req.session.get('user').get('email'), list(category.objects.all().values())))})

# დავალების დამატება
def add_new_task(req):
    if req.method == 'POST':
        task_model = taskForm(req.POST)

        if task_model.is_valid():
            item = task_model.save(commit=False)
            item.email = req.session['user'].get('email')
            item.category = req.POST['select']
            item.save()

    return redirect('tasks')

# ყველა დავალების ნახვა
def all_tasks(req):
    user_tsk = list(filter(lambda u: u['email'] == req.session['user'].get('email'), list(task.objects.all().values())))
    filter_value = '' 

    if req.method == 'POST':
        if req.POST['category_filter'].strip() and req.POST['category_filter'].strip() != 'All':
            user_tsk = task.objects.filter(category=req.POST['category_filter'])
            filter_value = req.POST['category_filter']
     
    return render(req, 'all_task.html', {
        'tasks': user_tsk,
        'category': category.objects.all().values(),
        'filter_value': filter_value
        })

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

# დაედითება
def edit(req, id):
    if req.session.get('user'):
        tsk = task.objects.all().get(id=id)
        user_tsk = list(filter(lambda u: u['email'] == req.session['user'].get('email'), list(task.objects.all().values())))
        if req.method == 'GET':
            return render(req, 'all_task.html', {
            'tasks': user_tsk,
            'is_edit': True
            })
        else:
            if req.POST['value'].strip():
                tsk.tasks = req.POST['value']
                tsk.save()
                return redirect('all')
            return render(req, 'all_task.html', {'message': 'Error'})
        
# კატეგორიებში დამატება
def add_category(req):
    if req.method == 'POST' and req.session.get('user'):
        if len(req.POST['category_name'].strip()) > 0:
            ctg = category.objects.filter(category = req.POST['category_name'].strip(), email = req.session.get('user')['email'])
            if ctg.count() > 0:
                return render(req, 'category.html', {'message': 'exist'})
            else:
                category(email=req.session.get('user')['email'], category=req.POST['category_name'].strip()).save()
        else:
            return render(req, 'category.html', {'message': 'must contain value'})
    return render(req, 'category.html')

# ყველა კატეგორიის ნახვა
def view_category(req):
    if req.session.get('user') :
        all_tsk = list(task.objects.filter(email = req.session.get('user').get('email')).values())
        is_asc = False
        
        obj = {}
        for tsk in all_tsk:
            if obj.get(tsk.get('category')):
               obj.get(tsk.get('category')).append(tsk.get('tasks'))
            else:
                obj[tsk['category']] = [tsk.get('tasks')] 

        for ctg in list(category.objects.all().values()):
            if ctg.get('category') not in obj.keys():
                obj[ctg.get('category')] = []

        if req.method == 'POST' :
            if 'asc' in req.POST: 
                obj = dict(sorted(obj.items()))
                is_asc = True
            else:
                obj = dict(sorted(obj.items(), reverse=True))
                is_asc = False

        return render(req, 'view_category.html', {
            'category': obj, 
            'tasks': all_tsk,
            'is_asc': is_asc
        })
    
# კატეგორიების წაშლა
def delete_category(req, ctg):
    if req.session.get('user'):
        category.objects.get(category=str(ctg)).delete()
        task.objects.filter(category=str(ctg)).delete()
        return redirect('view_category')
    
# კატეგორიების ედითი
def edit_category(req, ctg):
    if req.session.get('user'):
        main_category = category.objects.get(category=str(ctg))
        all_ctg = category.objects.all().values()
        all_tsk = task.objects.filter(category = ctg)
        
        if req.method == 'POST':
            if req.POST['value'].strip():
                main_category.category = req.POST['value']

                main_category.save()
                all_tsk.update(category = req.POST['value'])

                return redirect('view_category')
       
        else:
            return render(req, 'view_category.html', {
            'category': all_ctg,
            'is_edit': True
            })
    else:
        return redirect('tasks')
    
# ინფორმაცია
def view_task(req, id):
    if req.session.get('user'):
        try:
            tsk = task.objects.get(id = id)
            page = 'all_task.html'
        except:
            tsk = delt.objects.get(id = id)
            page = 'delete.html'

        tasks = task.objects.all().values()
        all_ctg = category.objects.all().values()

        if req.method == 'POST':
            new_ctg = req.POST['new_category']
            tsk.category = new_ctg
            tsk.save()

        return render(req, page, {
            'task': tsk,
            'is_open': True,
            'tasks': tasks,
            'category': all_ctg
        })
    
# 
# def filter_tsks(req, ctg):
#     if req.session.get('user'):

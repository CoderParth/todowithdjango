from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from todoapp.models import Task




# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account was successfuly created for {username}')
			return redirect('profile')
	else:
		form = UserRegisterForm()
		return render(request, 'users/register.html', {'form': form})

# for newly registered users
def home(request):
	return render(request, 'users/home.html')

@login_required
def profile(request):
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		context = {
					'u_form': u_form,
					'p_form': p_form,
					'tasks': request.user.task_set.all(),
					'range': range(1,6)
					}
		search_input = request.GET.get('search-input')
		clear_search = request.GET.get('clear')
		sort = request.GET.get('sort')

		#for sorting
		if sort:
			all_user_tasks = request.user.task_set.all()
			if sort == 'lowest to highest':
				sorted_task = all_user_tasks.order_by('priority')
			elif sort == 'highest to lowest':
				sorted_task = all_user_tasks.order_by('-priority')
			elif sort == 'None':
				context = {
					'u_form': u_form,
					'p_form': p_form,
					'tasks': request.user.task_set.all(),
					'range': range(1,6)
					}
				return render(request, 'users/profile.html', context)
			# using this context if sort exists..
			context = {
					'u_form': u_form,
					'p_form': p_form,
					'tasks': sorted_task,
					'range': range(1,6),
					'sort': sort

					}
			return render(request, 'users/profile.html', context)


		if clear_search:
			return render(request, 'users/profile.html', context)

		if search_input:
			all_user_tasks = request.user.task_set.all()
			filtered_task = all_user_tasks.filter(item__icontains=search_input)
			context = {
				'u_form': u_form,
				'p_form': p_form,
				'tasks': filtered_task,
				'range': range(1,6),
				'search_input': search_input
				}
			return render(request, 'users/profile.html', context)
		return render(request, 'users/profile.html', context)


#for updating user details
def edit_profile(request):
	if request.method == 'POST':
			u_form = UserUpdateForm(request.POST, instance=request.user)
			p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
			if u_form.is_valid() and p_form.is_valid():
				u_form.save()
				p_form.save()
				messages.success(request, f'Profile updated for {request.user.username}')
				return redirect('profile')
			else:
				u_form = UserUpdateForm(instance=request.user)
				p_form =ProfileUpdateForm(instance=request.user.profile)
				messages.error(request, f'Something went wrong')
				return redirect('profile')



def add_task(request):
	#For adding a task
	if request.method == 'POST':
		task = request.POST['task']
		priority = request.POST['priority']
		new_task = Task(item=task, priority=priority, author=request.user)
		if task != '' and priority != '':
			new_task.save()
		else:
			messages.error(request, 'Task cannot be an empty field')
		return redirect('profile')

# Edit a task
def edit_task(request):
	if request.method == 'GET':
		task_item = request.GET.get('task')
		task_priority = request.GET.get('priority')
		task_id = request.GET.get('task_id')
		print(task_id)
		context = {
			'task_item': task_item,
			'task_priority': task_priority,
			'task_id': task_id,
			'range': range(1,6)
		}
		return render(request, 'users/edit_task.html', context)

	if request.method == 'POST':

		task_item = request.POST['task']
		task_priority = request.POST['priority']
		task_id = request.POST['task_id']
		## Getting that task to edit
		task_to_edit = Task.objects.get(id=task_id)
		task_to_edit.item = task_item
		task_to_edit.priority = task_priority
		#saving the edited task
		task_to_edit.save()
		return redirect('profile')

		# if request.method == 'POST':
		# task_item = request.POST['task']
		# task_priority = request.POST['priority']
		# task_id = request.POST['task_id']
		# # Getting that task to edit
		# task_to_edit = Task.objects.get(id=task_id)
		# task_to_edit.item = task_item
		# task_to_edit.priority = task_priority
		# #saving the edited task
		# task_to_edit.save()
		# return redirect('profile')


def delete_task(request):
	if request.method == 'POST':
		task_id = request.POST['task_id']
		task_to_delete = Task.objects.get(id=task_id)
		task_to_delete.delete()
		print(task_to_delete)
	return redirect('profile')



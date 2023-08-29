from django.shortcuts import render, redirect
from .models import Project, Tags
from .utils import searchProject, paginateProjects
from .forms import ProjectForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'project/home.html')

def projects(request):
    projects, search_query = searchProject(request)

    custom_range, projects = paginateProjects(request, projects, 6)
    
    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'project/projects.html', context)

def single_projects(request, pk):
    projectobj = Project.objects.get(id=pk)
    form = ReviewForm() 

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectobj
        review.owner = request.user.profile
        review.save()

        projectobj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('single_projects', pk=projectobj.id)
    
    # tags = projectobj.tags.all()
    context = {'project': projectobj, 'form': form}
    return render(request, 'project/single_projects.html', context)


# this login decorator will restrict the un authenticated user to access this form or page
@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'project/project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'project/project_form.html', context)



@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {'obj': project}
    return render(request, 'delete_form.html', context)
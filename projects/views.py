from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages


from projects.forms import ProjectForm, ReviewForm
from projects.models import Project
from projects.utils import paginateProjects, searchProjects


def projects(request):

    search_query, projects = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)


    context = {'projects':projects, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.owner = request.user.profile
        review.project = project
        review.save()

        project.getVoteCount

        messages.success(request, 'Your review was succesfully submitted')
        return redirect('project', pk=project.id)

    context = {'project':project, 'form':form}
    return render(request, "projects/single-project.html", context)


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)  


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request, 'Project was deleted succesfully ')
        return redirect('projects')
    context = {'project':project}
    return render(request, "delete_template.html", context)  

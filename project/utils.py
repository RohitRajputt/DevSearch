from .models import Project, Tags
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProjects(request, projects, result):
    
    page = request.GET.get('page')
    paginator = Paginator(projects, result)

    try:
        projects = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    leftindex = (int(page) - 1)

    if leftindex < 1:
        leftindex = 1

    rightindex = (int(page) + 2)

    if rightindex > paginator.num_pages:
        rightindex = paginator.num_pages + 1

    custom_range = range(leftindex, rightindex)

    return custom_range, projects


def searchProject(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tag = Tags.objects.filter(name__icontains=search_query)


    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_query) |
        Q(description__icontains = search_query) |
        Q(owner__name__icontains = search_query) |
        Q(tags__in = tag)
    )
    return projects, search_query
from projects.models import Project, Comment, FavProject

from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from ads.utils import dump_queries
from projects.forms import CommentForm
from projects.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView




class ProjectListView(OwnerListView):
    template_name = "projects/list.html"

    def get(self, request) :
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_projects.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]

        strval =  request.GET.get("search", False)
        if strval :
            # __icontains for case-insensitive search

            query = Q(title__icontains=strval)  # Search in title
            query.add(Q(text__icontains=strval), Q.OR)  # Search in text
            query.add(Q(techs__icontains=strval), Q.OR)  # Search in techs (a CharField)
            query.add(Q(tags__name__icontains=strval), Q.OR)  # Search in tags (TaggableManager related field)
            query.add(Q(category__name__icontains=strval), Q.OR)  # Search in category name (ForeignKey)
            query.add(Q(requirement__name__icontains=strval), Q.OR)  # Search in requirement name (ForeignKey)
            query.add(Q(status__name__icontains=strval), Q.OR)  # Search in status name (ForeignKey)
            objects = Project.objects.filter(query).select_related().distinct().order_by('-updated_at')
        else :
            objects = Project.objects.all().order_by('-updated_at')

        # Augment the post_list
        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {'project_list' : objects, 'search': strval,'favorites': favorites,}
        retval = render(request, self.template_name, ctx)
        dump_queries()
        return retval

class ProjectDetailView(OwnerDetailView):
    model = Project
    template_name = "projects/detail.html"
    def get(self, request, pk) :
        x = Project.objects.get(id=pk)
        comments = Comment.objects.filter(project=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'project' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

from .forms import ProjectForm

class ProjectCreateView(OwnerCreateView):
    model = Project
    form_class = ProjectForm  # Use the custom form
    # fields = ['title', 'text', 'tags', 'repo', 'category', 'techs', 'requirement', 'status', 'notes']
    template_name = "projects/form.html"


class ProjectUpdateView(OwnerUpdateView):
    model = Project
    form_class = ProjectForm
    # fields = ['title', 'text', 'tags', 'repo', 'category', 'techs', 'requirement', 'status', 'notes']
    template_name = "projects/form.html"

class ProjectDeleteView(OwnerDeleteView):
    model = Project
    template_name = "projects/delete.html"

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Project, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, project=f)
        comment.save()
        return redirect(reverse('projects:project_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "projects/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        Project = self.object.Project
        return reverse('projects:project_detail', args=[Project.id])

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Project, id=pk)
        fav = FavProject(user=request.user, project=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Project, id=pk)
        try:
            FavProject.objects.get(user=request.user, project=t).delete()
        except FavProject.DoesNotExist:
            pass

        return HttpResponse()


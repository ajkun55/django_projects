from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from taggit.managers import TaggableManager


class Project(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(5, "Title must be greater than 5 characters")]
    )
    text = models.TextField()
    repo = models.URLField(
        max_length=200,
        blank=True,
        default="",
        help_text="Provide a valid URL for the project repository.",
    )
    # https://django-taggit.readthedocs.io/en/latest/api.html#TaggableManager
    tags = TaggableManager(blank=True, related_name='project_tags')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='project_owner')
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='project_comments')
    # Favorites
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='FavProject', related_name='favorite_projects')

    # category
    category = models.ForeignKey('Category',
        on_delete=models.CASCADE, related_name='project_category')

    # requirement
    requirement = models.ForeignKey('Requirement',
        on_delete=models.CASCADE, related_name='project_requirement')

    techs = models.CharField(
            max_length=200,blank=True,null=False,
            validators=[MinLengthValidator(2, "Tech must be greater than 2 characters")]
    )

    status = models.ForeignKey('Status',
        on_delete=models.CASCADE, related_name='project_status')

    notes = models.CharField(
            max_length=100, blank=True,null=True,
            validators=[MinLengthValidator(10, "Notes must be greater than 10 characters"),],default= ''
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.title

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='project_comment_owner')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'

class FavProject(models.Model) :
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/4.2/ref/models/options/#unique-together
    class Meta:
        unique_together = ('project', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.project.title[:10])

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Fullstack', 'Fullstack'),
    ]

    name = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        unique=True,
        verbose_name="Category Name"
    )


    def __str__(self):
        return self.name

class Requirement(models.Model):
    REQUIREMENT_CHOICES = [
        ('Junior', 'Junior'),
        ('Mid-level', 'Mid-level'),
        ('Advanced', 'Advanced'),
    ]

    name = models.CharField(
        max_length=50,
        choices=REQUIREMENT_CHOICES,default='Junior',
        unique=True,
        verbose_name="Requirement"
    )


    def __str__(self):
        return self.name

class Status(models.Model):
    REQUIREMENT_CHOICES = [
        ('Add-To-Do-List', 'Add-To-Do-List'),
        ('In-Progress', 'In-Progress'),
        ('Done', 'Done'),
    ]

    name = models.CharField(
        max_length=50,
        choices=REQUIREMENT_CHOICES,default='Done',
        unique=True,
        verbose_name="Status"
    )


    def __str__(self):
        return self.name


# class Tech(models.Model):

#     # name = models.JSONField(
#     #     default=list,  # Default to an empty list
#     #     verbose_name="List of Technologies"
#     # )
#     name = models.CharField(max_length=100)
#     # project = models.ManyToManyField('Project',through='ProjectTech',related_name='project_tech')

#     def __str__(self):
#         return self.name



# class ProjectTech(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     tech = models.ForeignKey(Tech, on_delete=models.CASCADE)
#     class Meta:
#         unique_together = ('project', 'tech')
#     def __str__(self):
#         return f"{self.project} - {self.tech}"

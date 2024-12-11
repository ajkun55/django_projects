import csv  # https://docs.python.org/3/library/csv.html

from django.contrib.auth import get_user_model
from projects.models import Project, Category, Requirement, Status

User = get_user_model()
owner = User.objects.get(username='admin')

def run():
    print("=== Polls Loader")

    Project.objects.all().delete()
    print("=== Objects deleted")

    # Open the CSV file containing project data
    with open('scripts/projects.csv', newline='', encoding='utf-8') as fhand:
        reader = csv.DictReader(fhand)  # Use DictReader to read CSV with header mapping to column names

        for row in reader:
            print(f"Processing project: {row['title']}")

            # Get or create related objects for ForeignKey fields
            category = Category.objects.get(name=row['category'])  # Assuming 'category' in CSV corresponds to Category name
            requirement = Requirement.objects.get(name=row['requirement'])  # Assuming 'requirement' corresponds to title
            status = Status.objects.get(name=row['status'])  # Assuming 'status' corresponds to Status name

            # Create or get the Project object
            project, created = Project.objects.get_or_create(
                title=row['title'],
                text=row['text'],
                repo=row['repo'],
                category=category,
                requirement=requirement,
                status=status,
                owner=owner,
                techs=row['techs'] or '',  # Handle empty techs (can be empty string)
                notes=row['notes'] or '',  # Handle empty notes (can be empty string)
            )

            # # Handle ManyToMany fields (comments and favorites)
            # if row['comments']:  # Check if there are comments
            #     comment_usernames = row['comments'].split(',')  # Assuming comments are comma-separated usernames
            #     for username in comment_usernames:
            #         try:
            #             user = User.objects.get(username=username.strip())
            #             project.comments.add(user)  # Add user to comments
            #         except User.DoesNotExist:
            #             print(f"Warning: User {username} does not exist for comments.")

            # if row['favorites']:  # Check if there are favorites
            #     favorite_usernames = row['favorites'].split(',')  # Assuming favorites are comma-separated usernames
            #     for username in favorite_usernames:
            #         try:
            #             user = User.objects.get(username=username.strip())
            #             project.favorites.add(user)  # Add user to favorites
            #         except User.DoesNotExist:
            #             print(f"Warning: User {username} does not exist for favorites.")

            # Save the project instance (required after modifying ManyToMany fields)
            project.save()

    # fhand = open('scripts/projects.csv')
    # reader = csv.reader(fhand)
    # next(reader)  # Advance past the header

    # for row in reader:
    #     print(row)

    #     # Make a new Question and save it
    #     # q, created = Question.objects.get_or_create(question_text=row[0],pub_date=timezone.now() - datetime.timedelta(days=1))
    #     # q.save()
    #     p, created = Question.objects.get_or_create(title=row[0],text=row[1],repo=row[2],category=row[3], requirement=row[4], status=row[5])
    #     p.save()
    #     # Loop through the choice strings in row[1:] and add each choice,
    #     # connect it to the question and save it



    print("=== Load Complete")
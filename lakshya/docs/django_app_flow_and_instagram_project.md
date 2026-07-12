# Django App Flow Guide and Instagram Project Plan

## 1. What This Current App Does

This project is a simple job board called `CareerHub`.

Main use cases:

- A visitor can see job posts.
- A visitor can search jobs by title, company name, or location.
- A visitor can register an account.
- A user can log in.
- A logged-in user can create a job.
- A logged-in user can edit a job.
- A logged-in user can delete a job.
- A logged-in user can log out.

This is a good beginner Django project because it teaches:

- URL routing
- Views
- Templates
- Models
- Forms
- Database queries
- Authentication
- Login/logout
- File uploads
- Conditional UI
- Search with `Q` objects

## 2. How A Django Request Works

When you open a URL in the browser, Django follows this flow:

```text
Browser URL
   ↓
Project urls.py
   ↓
App urls.py
   ↓
View function
   ↓
Model/database if needed
   ↓
Template
   ↓
HTML response back to browser
```

Example:

```text
http://127.0.0.1:8000/
   ↓
lakshya/urls.py
   ↓
myapp/urls.py
   ↓
home view
   ↓
Job.objects.all()
   ↓
index.html
   ↓
Job cards shown in browser
```

## 3. Important Files In Your Project

### `manage.py`

This file runs Django commands.

Common commands:

```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py check
```

### `lakshya/settings.py`

This is the main configuration file.

Important things inside it:

- `INSTALLED_APPS`: tells Django which apps are active.
- `DATABASES`: tells Django which database to use.
- `TEMPLATES`: tells Django how to find HTML templates.
- `MEDIA_URL` and `MEDIA_ROOT`: used for uploaded images.
- `LOGIN_URL`: where Django sends users who are not logged in.
- `LOGIN_REDIRECT_URL`: where users go after login.
- `LOGOUT_REDIRECT_URL`: where users go after logout if using built-in logout.

### `lakshya/urls.py`

This is the project-level URL file.

It sends requests to:

- Django admin
- Your app URLs
- Django auth URLs
- Media file serving in development

Example:

```python
path('', include('myapp.urls'))
```

This means your app controls the home page and app routes.

### `myapp/models.py`

This file defines database tables.

Your current model:

```python
class Job(models.Model):
    title = models.CharField(max_length=255)
    companyName = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.IntegerField()
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
```

This creates a `Job` table in the database.

Each job has:

- title
- company name
- location
- salary
- optional company logo

### `myapp/urls.py`

This file connects URLs to view functions.

Examples:

```python
path('', home, name='home')
path('createjob/', createjob, name='createjob')
path('register/', register, name='register')
path('logout/', logout_user, name='logout_user')
```

The `name` is important because templates can use it:

```django
{% url 'home' %}
```

This is better than hardcoding URLs.

### `myapp/views.py`

Views contain the logic.

A view receives a request and returns a response.

Common view pattern:

```python
def home(request):
    jobs = Job.objects.all()
    return render(request, 'index.html', {'jobs': jobs})
```

This means:

- Get all jobs.
- Open `index.html`.
- Send `jobs` to the template.
- Return HTML to the browser.

### `myapp/forms.py`

This file contains Django forms.

Your `UserRegistrationForm` extends `UserCreationForm`.

It adds an email field:

```python
email = forms.EmailField(required=True)
```

It also saves the email to the user:

```python
user.email = self.cleaned_data['email']
```

### `templates/base.html`

This is the shared layout.

It contains:

- HTML head
- Tailwind/DaisyUI links
- Navbar
- Search form
- Login/register buttons
- User dropdown
- Logout form
- `{% block content %}` for page content

Other templates extend it:

```django
{% extends 'base.html' %}
```

### `templates/index.html`

This page shows job cards.

It loops through jobs:

```django
{% for job in jobs %}
```

It conditionally shows edit/delete buttons:

```django
{% if user.is_authenticated %}
```

This means only logged-in users can see those controls.

## 4. Registration Flow

URL:

```text
/register/
```

Flow:

```text
User opens /register/
   ↓
register view creates empty form
   ↓
register.html displays form
   ↓
User submits form
   ↓
register view validates form
   ↓
User is saved
   ↓
User is redirected to login page
```

Important code idea:

```python
form = UserRegistrationForm(request.POST)
if form.is_valid():
    user = form.save(commit=False)
    user.save()
```

`commit=False` means:

- Create the user object.
- Do not save it to the database yet.
- Give yourself a chance to modify it.
- Then call `user.save()`.

In your app, it is useful for learning. In a very simple registration form, `form.save()` would also work.

## 5. Login Flow

Your project uses Django's built-in login view:

```python
path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login')
```

Flow:

```text
User opens /accounts/login/
   ↓
Django LoginView displays login.html
   ↓
User submits username and password
   ↓
Django checks credentials
   ↓
If correct, user session is created
   ↓
User is redirected to /
```

Important field names in login form:

```html
name="username"
name="password"
```

Django expects those names.

## 6. Logout Flow

Navbar form:

```django
<form action="{% url 'logout_user' %}" method="post">
  {% csrf_token %}
  <button type="submit">Logout</button>
</form>
```

View:

```python
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('/')
```

Flow:

```text
User clicks Logout
   ↓
POST request goes to /logout/
   ↓
logout_user view runs
   ↓
Django clears the session
   ↓
User redirects to /
```

## 7. Search Flow

Search form in navbar:

```django
<form action="{% url 'home' %}" method="get">
  <input type="text" name="query" value="{{ query|default:'' }}" />
</form>
```

When the user searches `python`, the URL becomes:

```text
/?query=python
```

View:

```python
query = request.GET.get('query', '')
jobs = Job.objects.all()

if query:
    jobs = jobs.filter(
        Q(title__icontains=query) |
        Q(companyName__icontains=query) |
        Q(location__icontains=query)
    )
```

Meaning:

- `request.GET.get('query')` reads the search text.
- `icontains` means case-insensitive contains.
- `Q` lets you search multiple fields with OR logic.

Search examples:

- Search by title: `developer`
- Search by company: `Google`
- Search by location: `Delhi`

## 8. Create Job Flow

URL:

```text
/createjob/
```

Protected by:

```python
@login_required
```

This means:

- Logged-in users can open it.
- Logged-out users are sent to login.

Flow:

```text
User opens /createjob/
   ↓
If not logged in, redirect to login
   ↓
If logged in, show addform.html
   ↓
User submits job details
   ↓
View creates Job object
   ↓
Job is saved
   ↓
Redirect to home
```

Important because the form has file upload:

```html
enctype="multipart/form-data"
```

Without this, image upload will not work.

## 9. Update Job Flow

URL:

```text
/update/<job_id>/
```

Example:

```text
/update/3/
```

Flow:

```text
Find job by id
   ↓
Show update form
   ↓
User submits changes
   ↓
Update fields
   ↓
Save job
   ↓
Redirect home
```

Current code:

```python
job = Job.objects.get(id=id)
```

Beginner note:

In production, prefer:

```python
from django.shortcuts import get_object_or_404
job = get_object_or_404(Job, id=id)
```

Because it shows a proper 404 page if the job does not exist.

## 10. Delete Job Flow

URL:

```text
/delete/<job_id>/
```

Flow:

```text
User clicks Delete
   ↓
Browser asks confirm
   ↓
POST request goes to delete view
   ↓
Job is deleted
   ↓
Redirect home
```

Delete is protected with:

```python
@login_required
```

And the template uses CSRF:

```django
{% csrf_token %}
```

This protects against fake delete requests from other websites.

## 11. Things Every Beginner Should Know

### URL Names Are Important

Use:

```django
{% url 'home' %}
```

Instead of:

```html
href="/"
```

This makes your app easier to change later.

### GET vs POST

Use GET for:

- Search
- Filtering
- Reading pages

Use POST for:

- Login
- Register
- Create
- Update
- Delete
- Logout

### CSRF Token

Every POST form should include:

```django
{% csrf_token %}
```

### `request.GET`

Used for query parameters:

```text
/?query=python
```

Read it like:

```python
request.GET.get('query')
```

### `request.POST`

Used for submitted form data:

```python
request.POST.get('title')
```

### `request.FILES`

Used for uploaded files:

```python
request.FILES.get('logo')
```

### `@login_required`

Use this when only logged-in users should access a view.

```python
@login_required
def createjob(request):
    ...
```

### Template Conditions

Use this to change UI based on login state:

```django
{% if user.is_authenticated %}
  Show private buttons
{% else %}
  Show login/register
{% endif %}
```

### Django ORM

ORM means you write Python instead of SQL.

Examples:

```python
Job.objects.all()
Job.objects.filter(title__icontains='python')
Job.objects.get(id=1)
job.save()
job.delete()
```

## 12. Suggested Improvements For This Job Board

Good next improvements:

1. Use `get_object_or_404` for update/delete.
2. Use Django `ModelForm` for create/update job forms.
3. Add job description field.
4. Add job type field: full-time, part-time, internship.
5. Add created date.
6. Connect each job to the user who created it.
7. Only allow the job owner to edit/delete their own jobs.
8. Add pagination.
9. Add better search filters.
10. Add user profile page.

## 13. Instagram-Like Django Project Plan

Project name idea:

```text
Snapgram
```

Core features:

- Register
- Login
- Logout
- Profile page
- Upload image post
- Show feed
- Like post
- Comment on post
- Follow/unfollow users
- Search users
- Edit profile

## 14. Instagram Project Models

You can create these models:

### Profile

Purpose:

Stores extra user details.

Fields:

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', default='default.png')
```

### Post

Purpose:

Stores uploaded photos.

Fields:

```python
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Like

Purpose:

Tracks which user liked which post.

Fields:

```python
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
```

### Comment

Purpose:

Stores comments on posts.

Fields:

```python
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Follow

Purpose:

Tracks user following relationships.

Fields:

```python
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
```

## 15. Instagram Project URL Plan

```python
urlpatterns = [
    path('', feed, name='feed'),
    path('register/', register, name='register'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_user, name='logout_user'),
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('post/create/', create_post, name='create_post'),
    path('post/<int:id>/', post_detail, name='post_detail'),
    path('post/<int:id>/like/', like_post, name='like_post'),
    path('post/<int:id>/comment/', add_comment, name='add_comment'),
    path('follow/<str:username>/', follow_user, name='follow_user'),
    path('search/', search_users, name='search_users'),
]
```

## 16. Instagram Project Page Flow

### Feed Page

Shows posts from all users or followed users.

Flow:

```text
Open /
   ↓
Get posts from database
   ↓
Show posts newest first
```

### Create Post Page

Flow:

```text
Logged-in user opens /post/create/
   ↓
Select image and caption
   ↓
Submit form
   ↓
Save post
   ↓
Redirect to feed
```

### Profile Page

Flow:

```text
Open /profile/lakshya/
   ↓
Find user by username
   ↓
Show profile info
   ↓
Show user's posts
   ↓
Show follow/unfollow button
```

### Like Flow

Flow:

```text
Click Like
   ↓
If like exists, remove it
   ↓
If like does not exist, create it
   ↓
Redirect back
```

### Comment Flow

Flow:

```text
Write comment
   ↓
Submit POST form
   ↓
Create Comment object
   ↓
Redirect to post detail
```

### Follow Flow

Flow:

```text
Click Follow
   ↓
Create Follow object
   ↓
Button changes to Unfollow
```

## 17. Instagram Project Build Order

Build in this order:

1. Create Django project and app.
2. Configure templates, static, and media.
3. Add register/login/logout.
4. Create `Profile` model.
5. Auto-create profile when user registers.
6. Create `Post` model.
7. Build create post page.
8. Build feed page.
9. Build profile page.
10. Add like model and like button.
11. Add comment model and comment form.
12. Add follow model.
13. Add search users.
14. Improve UI with Tailwind.
15. Add permissions so users only edit/delete their own posts.

## 18. Beginner Mistakes To Avoid

- Do not forget `{% csrf_token %}` in POST forms.
- Do not forget `enctype="multipart/form-data"` for image uploads.
- Do not hardcode URLs when `{% url %}` can be used.
- Do not show edit/delete buttons to everyone.
- Do not trust only the frontend. Protect views with `@login_required`.
- Do not use `get()` without handling missing objects in bigger projects.
- Do not store uploaded files in the wrong folder.
- Do not forget to run migrations after model changes.

## 19. Commands You Will Use Often

```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py check
```

## 20. Final Beginner Mental Model

Think of Django like this:

```text
models.py = database structure
urls.py = road map
views.py = brain/logic
templates = HTML pages
forms.py = form validation and saving
settings.py = project configuration
```

If you understand these six parts, you can build most beginner Django apps.


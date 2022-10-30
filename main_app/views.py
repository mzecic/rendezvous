from django.shortcuts import render, redirect
from .models import Listing, Photo
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from datetime import date
import uuid
import boto3
import os

# Test listings data


# listings = [
#   Listing('title1', 'description1'),
#   Listing('title2', 'description2'),
#   Listing('title3', 'description3'),
#   ]

# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def listings_index(request):
    listings = Listing.objects.all()
    return render(request, 'listings/index.html', { 'listings': listings })

def listings_detail(request, listing_id):
  listing = Listing.objects.get(id=listing_id)
  # print('signed in user id', request.user.id, 'owner', listing.user.id)
  comment_form = CommentForm()
  return render(request, 'listings/detail.html', { 'listing': listing, 'comment_form':comment_form})

def add_comment(request, listing_id):
   # create a ModelForm instance using the data in request.POST
  form = CommentForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_comment = form.save(commit=False)
    new_comment.listing_id = listing_id
    new_comment.date = date.today()
    new_comment.commenter_id = request.user.id
    new_comment.save()
  return redirect('detail', listing_id=listing_id)

class ListingCreate(LoginRequiredMixin, CreateView):
  model = Listing
  fields = ['title', 'description', 'price']
  success_url = '/listings/'

  def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user
        # Let the CreateView do its job as usual
        return super().form_valid(form)

class ListingUpdate(LoginRequiredMixin, UpdateView):
  model = Listing
  fields = ['title', 'description', 'price']


class ListingDelete(LoginRequiredMixin, DeleteView):
  model = Listing
  success_url = '/listings/'


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def add_photo(request, listing_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, listing_id=listing_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', listing_id=listing_id)
from django.shortcuts import render, redirect, reverse
from .models import Listing, Photo, Comment, User, Profile
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
#gmaps stuff
import googlemaps
from datetime import datetime

# import requests
# import json
# import pandas as pd
# import urllib.request
# import simplejson as json
# import pprint
# import environ

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

def my_listings(request):
    listings = Listing.objects.all()
    return render(request, 'listings/my_listings.html', {'listings': listings })

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
      profile = Profile.objects.create(user_id=user.id)
      profile.save()
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

def delete_comment(request, comment_id, listing_id):
  # comment = get_object_or_404(Comment, comment=comment_id)
  if request.user.is_superuser:
    Comment.objects.get(pk=comment_id).delete()

  return redirect(reverse('detail', args=(listing_id,)))


def profile_edit(request, user_id):
  user = User.objects.get(id=user_id)
  profile = Profile.objects.get(user=user_id)
  return render(request, 'profile/detail.html', {
    'user': user,
    'user': request.user,
    'profile': profile
  })

# gmaps
def maps_sandbox(request):
  g_api_key = os.environ['GOOGLE_API_KEY']
  gmaps = googlemaps.Client(key=g_api_key)
  # Geocoding an address
  # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
  geocode_result = gmaps.geocode('1858 Ashland Ave, St. Paul, MN')
  coordinates = geocode_result[0]["geometry"]["location"]

  elements = []
  for i in geocode_result[0]["address_components"]:
    elements.append( i["long_name"] )

  elements.append( str(coordinates['lat']) ) # convert to string to use `join`
  elements.append( str(coordinates['lng']) ) # convert to string to use `join`

  lat = str(coordinates['lat'])
  lng = str(coordinates['lng'])
  full_address = ", ".join(elements)
  # Look up an address with reverse geocoding
  # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

  # Request directions via public transit
  # now = datetime.now()
  # directions_result = gmaps.directions("Sydney Town Hall",
  #                                     "Parramatta, NSW",
  #                                     mode="transit",
  #                                     departure_time=now)

  return render(request,'maps/sandbox.html',
                {
                # 'geocode_result': ", ".join(elements),
                # 'reverse_geocode_result':reverse_geocode_result,
                # 'directions_result':directions_result,
                'lat':lat,
                'lng':lng,
                'full_address':full_address,
                'g_api_key':g_api_key})

from django.shortcuts import render, redirect, reverse
from .models import Listing, Photo, Comment, User, Profile
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .forms import CommentForm
from datetime import date
import uuid
import boto3
import os
#gmaps stuff below
import googlemaps
from datetime import datetime


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
  comment_form = CommentForm()
  return render(request, 'listings/detail.html', { 'listing': listing, 'comment_form':comment_form})

def add_comment(request, listing_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    # don't save the form to the db until it
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
        form.instance.user = self.request.user
        return super().form_valid(form)

class ListingUpdate(LoginRequiredMixin, UpdateView):
  model = Listing
  fields = ['title', 'description', 'price',]


class ListingDelete(LoginRequiredMixin, DeleteView):
  model = Listing
  success_url = '/listings/'

def add_photo(request, listing_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, listing_id=listing_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', listing_id=listing_id)

def edit_photos(request, listing_id):
  listing = Listing.objects.get(id=listing_id)
  photos = Photo.objects.filter(listing=listing_id)
  return render(request, 'listings/edit_photos.html', {'photos': photos, 'listing': listing})

def delete_photo(request, photo_id, listing_id):
  Photo.objects.get(pk=photo_id).delete()

  return redirect(reverse('edit_photos', args=(listing_id,)))

def delete_comment(request, comment_id, listing_id):
  if request.user.is_superuser:
    Comment.objects.get(pk=comment_id).delete()

  return redirect(reverse('detail', args=(listing_id,)))

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      profile = Profile.objects.create(user_id=user.id)
      profile.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def profile_edit(request, user_id):
  user = User.objects.get(id=user_id)
  profile = Profile.objects.get(user=user_id)
  return render(request, 'profile/detail.html', {
    'user': user,
    'profile': profile,
    'g_api_key':os.environ['GOOGLE_API_KEY']
  })

def profile_save(request, profile_id):
  profile = Profile.objects.get(id=profile_id)
  profile.location = request.POST.get("location")
  profile.address_line_1 = request.POST.get("address1")
  profile.city = request.POST.get("locality")
  profile.state = request.POST.get("state")
  profile.postal_code = request.POST.get("postcode")
  profile.country = request.POST.get("country")
  profile.save()
  return redirect(f'/profile/{request.user.id}')



# gmaps
def maps_sandbox(request):
  g_api_key = os.environ['GOOGLE_API_KEY']
  gmaps = googlemaps.Client(key=g_api_key)
  # Geocoding an address
  geocode_result = gmaps.geocode('1858 Ashland Ave, St. Paul, MN')
  coordinates = geocode_result[0]["geometry"]["location"]
  lat = str(coordinates['lat'])
  lng = str(coordinates['lng'])

  elements = []
  for i in geocode_result[0]["address_components"]:
    elements.append( i["long_name"] )

  elements.append(lat)
  elements.append(lng)

  full_address = ", ".join(elements)

  return render(request,'maps/sandbox.html',
                {
                'lat':lat,
                'lng':lng,
                'full_address':full_address,
                'g_api_key':g_api_key})

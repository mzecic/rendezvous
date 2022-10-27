from django.shortcuts import render
from .models import Listing
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Listing

# Test listings data


# listings = [
#   Listing('title1', 'description1'),
#   Listing('title2', 'description2'),
#   Listing('title3', 'description3'),
#   ]

# Add the following import
from django.http import HttpResponse

# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
    return HttpResponse('<h1>About the CatCollector</h1>')

def about(request):
  return render(request, 'about.html')

def listings_index(request):
    listings = Listing.objects.all()
    return render(request, 'listings/index.html', { 'listings': listings })

def listings_detail(request, listing_id):
  listing = Listing.objects.get(id=listing_id)
  return render(request, 'listings/detail.html', { 'listing': listing})

class ListingCreate(CreateView):
  model = Listing
  fields = ['title', 'description']
  success_url = '/listings/'
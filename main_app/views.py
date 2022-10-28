from django.shortcuts import render, redirect
from .models import Listing
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
  print('signed in user id', request.user.id, 'owner', listing.user.id)
  return render(request, 'listings/detail.html', { 'listing': listing})


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

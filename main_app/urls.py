from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('listings/', views.listings_index, name='index'),
    path('my_listings/', views.my_listings, name='my_listings'),
    path('listings/<int:listing_id>/', views.listings_detail, name='detail'),
    path('listings/create/', views.ListingCreate.as_view(), name='listings_create'),
    path('listings/<int:pk>/update/', views.ListingUpdate.as_view(), name='listings_update'),
    path('listings/<int:pk>/delete/', views.ListingDelete.as_view(), name='listings_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    # path('listings/<int:listing_id>/add_comment/<int:commenter_id>', views.add_comment, name='add_comment'),
    path('listings/<int:listing_id>/add_comment/', views.add_comment, name='add_comment'),
    path('listings/<int:listing_id>/add_photo/', views.add_photo, name='add_photo'),
    path('listings/<int:listing_id>/delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('maps/', views.maps_sandbox, name='maps_sandbox'),
    path('profile/<user_id>/', views.profile_edit, name="profile_edit"),
    path('profile/<int:profile_id>/save', views.profile_save, name="profile_save"),
    path('listing/<int:listing_id>/edit_photos/', views.edit_photos, name="edit_photos"),
    path('listings/<int:listing_id>/delete_photo/<int:photo_id>', views.delete_photo, name='delete_photo'),
]


let autocomplete;
function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('autocomplete'), 
    {
        componentRestrictions: { country: "us" },  // Apologies to my Canadian friend Abdullahi and Croatian friend Matej
        fields: ["address_components", "name", "place_id", "geometry"],
        types: ["address"],
    })
    autocomplete.addListener("place_changed", fillInAddress);
}

google.maps.event.addDomListener(window, 'load', initAutocomplete);
//defining place outside fillinaddress
let place 

function fillInAddress() {
    // Get the place details from the autocomplete object.
    
    place = autocomplete.getPlace();
    console.log('place', place)
    console.log('place ID****',place.place_id)

    let address1 = "";
    let postcode = "";
  
    // Get each component of the address from the place details,
    // and then fill-in the corresponding field on the form.
    // place.address_components are google.maps.GeocoderAddressComponent objects
    // which are documented at http://goo.gle/3l5i5Mr

    for (const component of place.address_components) {
      const componentType = component.types[0];
  
      switch (componentType) {
        case "street_number": {
          address1 = `${component.long_name} ${address1}`;
          break;
        }
      
        case "route": {
          address1 += component.short_name;
          document.querySelector("#address1").value = address1;
          break;
        }
  
        case "postal_code": {
          postcode = `${component.long_name}${postcode}`;
          break;
        }
  
        case "postal_code_suffix": {
          postcode = `${postcode}-${component.long_name}`;
          document.querySelector("#postcode").value = postcode;
          break;
        }
        case "locality":
          document.querySelector("#locality").value = component.long_name;
          break;
        case "administrative_area_level_1": {
          document.querySelector("#state").value = component.short_name;
          break;
        }
        case "country":
          document.querySelector("#country").value = component.long_name;
          break;
      }
    }
    initializeMap();
  
  }
//   // create map
  
  // var myCenter=new google.maps.LatLng(lat,lng);

  function initializeMap()
  {
  var mapProp = {
    // center:myCenter,
    zoom:2,
    mapTypeId:google.maps.MapTypeId.ROADMAP
    };

  var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);

  if (!place.geometry || !place.geometry.location) {
    return;
  }

  if (place.geometry.viewport) {
    map.fitBounds(place.geometry.viewport);
  } else {
    map.setCenter(place.geometry.location);
    map.setZoom(10);
  }

var marker=new google.maps.Marker({
  // position:myCenter,

  });

  marker.setPlace({
    placeId: place.place_id,
    location: place.geometry.location,
  });

  // google.maps.LatLng
  marker.setMap(map);
  }

  //what does this do??
window.initAutocomplete = initAutocomplete;


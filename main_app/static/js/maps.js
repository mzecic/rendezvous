
// let autocomplete = null;
let autocomplete;
function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('autocomplete'), 
    {
        componentRestrictions: { country: "us" },  // Apologies to my Canadian friend Abdullahi and Croatian friend Matej
        fields: ["address_components", "name"],
        types: ["address"],
    })
    autocomplete.addListener("place_changed", fillInAddress);
}

google.maps.event.addDomListener(window, 'load', initAutocomplete);

function fillInAddress() {
    // Get the place details from the autocomplete object.
    const place = autocomplete.getPlace();

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
      // bring map back when implementation is ready
      // initializeMap();
    }
  
  }
  
  window.initAutocomplete = initAutocomplete;


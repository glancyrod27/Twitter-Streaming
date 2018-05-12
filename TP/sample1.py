# from googlemaps import GoogleMaps
# gmaps = GoogleMaps(AAIzaSyDdJK0gaxyg-zmBV2GsnFmA61CcPuQak2I)
# lat, lng = gmaps.address_to_latlng("Philadelphia, PA")
# print lat
# print lng

from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("Philadelphia, PA")
print(location.address)
print((location.latitude, location.longitude))


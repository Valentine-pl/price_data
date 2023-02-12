from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExerciser")


def get_coordinates(branch):
    location = geolocator.geocode(branch)
    if location:
        return location.latitude, location.longitude
    else:
        return None

from geopy.geocoders import Nominatim

def get_location(latitude, longitude):
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse(f"{latitude}, {longitude}")
    return str(locname).split(',')
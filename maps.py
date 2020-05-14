"""
Uses the Google Maps Static API to generate an image of input location.
"""
import requests


def get_map(loc, zoom):
    key = "" #API KEY HERE
    
    loc = loc.replace(" ", "+")
    
    url = "https://maps.googleapis.com/maps/api/staticmap?center=" + loc + "&zoom=" + str(zoom) + "&size=640x640&markers=size:medium%7Ccolor:0xff0000%7Clabel:%7C" + loc + "&maptype=hybrid&key=" + key
    
    r = requests.get(url)
    file = open("map.png", "wb")
    file.write(r.content)
    file.close()


def edit_result(result):
    """Turns speech input into just the location. 
        Two possible inputs (for now): "where is ..." and "show me where ... is"
    """
    
    if "where is" in result:
        return result[8:].strip()
    else:
        begwhere = result.find("where")
        endis = result.rfind("is")
        return result[begwhere + 5:endis].strip()

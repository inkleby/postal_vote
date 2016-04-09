"""
Elevation Model - -
"""
import gdal
from gdalconst import GA_ReadOnly
import struct
from PIL import  Image, ImageDraw, ImageFont
from nav import lat_long_distance
import pyproj

class IsisCube(object):
    """
    open a cube file to extract elevation locations from it
    """
    def __init__(self,filename,conversion = lambda x : x):
        """
        accepts a filename and a lambda conversion - if points need to be adjusted
        before being returned (e.g. if points are exxagerated by 2 and have an offset of 10000 (lambda x : (x * 0.5) + 10000)
        """
        self.isis = gdal.Open(filename, GA_ReadOnly)

        self.width =  self.isis.RasterXSize
        self.height = self.isis.RasterYSize
        
        self.degree_h = float(self.width)/360
        self.degree_v = float(self.height)/180
        self.conversion = conversion

    def get_x_y(self,lat,lng):
        """
        given lat long convert to local coordinates
        """
        if lng > 180:
            lng = lng-360

        if lat > 90:
            lat = lat-180
            
        if lat < -90:
            lat = 180 + lat
            
        if lat < -180:
            lat = 360 + lat
        
        x = int((lng + 180) * self.degree_h)
        y = int((lat + 90) * self.degree_v)
        
        y = self.height - y #flip to count from top rather than bottom
        
        if x >= self.width:
            x -=1
        if y >= self.height:
            y -=1        
        
        return x, y
    
    

    def point(self,lat,lng):
        """
        Get value of a point - sourced from 
        http://gis.stackexchange.com/
        questions/46893/
        how-do-i-get-the-pixel-value-of-a-gdal-raster-under-an-ogr-point-without-numpy
        """
        if lat != lat or lng != lng:
            return None
        x,y = self.get_x_y(lat,lng)
        b = self.isis.GetRasterBand(1)
        structval = b.ReadRaster(x,y,1,1,buf_type=gdal.GDT_Int16)
        try:
            intval = struct.unpack('h' , structval) 
        except struct.error:
            return None
            
        
        v = intval[0]
        
        return self.conversion(v)

    
def get_moon_elevation(list_of_lat_long):
    """
    given a list of lats and longs will return eelvation oints from moon's service
    """
    lunar_cab = "E:\\lunar.cub" #sub your location here
    
    # source http://astrogeology.usgs.gov/search/details/Moon/LRO/LOLA/Lunar_LRO_LOLA_Global_LDEM_118m_Mar2014/cub
    i = IsisCube(lunar_cab, conversion =  lambda x: (x * 0.5) ) #LRO data is adjusted by 0.5 (and offset against radius 1737400)

    results = []
    for l in list_of_lat_long:
        p = i.point(*l)
        if p <> None:
            results.append(p)
    
    return results
 
 
def get_intermediate_points(start_lat,start_long,end_lat,end_long,points = 500):
    """
    given two lat and long points return points between
    """
    g = pyproj.Geod(ellps='sphere')

    lonlats = g.npts(start_long,start_lat, end_long, end_lat,
                     points)
    
    lonlats.insert(0,(start_long,start_lat))
    lonlats.append((end_long,end_lat))

        
    latlongs = [tuple(reversed(x)) for x in lonlats]

    return latlongs

def human_travel(hours):
    """
    makes decimal hours more human
    """
    import math
    
    m = int((hours % 1) * 60)
    h = int(math.floor(hours))
    if h > 24:
        d = int(math.floor(h/24))
        h = h % 24
    else:
        d = 0
        
    st = ""
    
    if d:
        st += "{0} Day".format(d)
        if d > 1:
            st += "s"
    if h:
        st += " {0} Hour".format(h)
        if h > 1:
            st += "s"
    if m and not d:
        st += " {0} Minute".format(m)
        if m > 1:
            st += "s"
            
    if st == "":
        st = "1 Minute"
    st = st.strip()
    return st
        

def illustrate(points,poi=None,objs=[],time=0,total_distance=0):
    """
    assumes three points (last, here, next) - will generate the graphic for this route. 
    """
    

    length=len(points)
    
    #points = [0-x for x in points]
    mi = min(points) - 100
    ma = max(points) - mi + 500
    diff = ma -400
    height=630 #hardcoded height of image
    
    
    #path distance 
    prev,here,next = objs
    if next:
        distance = round(here.distance(next)[0],1)
    else:
        distance = None
    if prev:
        prev_distance = round(prev.distance(here)[0],1)
    else:
        prev_distance = None
        
    if distance == None:
        distance = prev_distance
    if prev_distance == None:
        prev_distance = distance
        
    total_dist = distance + prev_distance
    pixel_per_meter = length/(float(total_dist)*1000)
    vertical_exaggeration = int(diff/100)
    if vertical_exaggeration > 25:
        vertical_exaggeration = 25
    #work out our vertical exaggeration
    if total_dist < 100:
        vertical_exaggeration = 15
    if total_dist < 100:
        vertical_exaggeration = 10
    if total_dist < 10:
        vertical_exaggeration = 5
            
    if pixel_per_meter > 0.1: #on small distances - less exaggeration
        vertical_exaggeration = 1
    
    pixel_adjust = height* pixel_per_meter * vertical_exaggeration
    
    
    #adjust moon data to fit image
    convert = lambda x: height - int(((float(x) - mi)/ma) * pixel_adjust) 
    
    #create image
    size = (length,height)
    im = Image.new('RGB', size) 
    draw = ImageDraw.Draw(im)
    

    #add captioning

    if len(poi) == 2 and total_distance == 0:
        midpoint = poi[0]
    else:
        midpoint = poi[1]
    
    
    current_height = points[midpoint]
    final_height = points[-1]
    diff = final_height-current_height
    if diff >= 0:
        desc = "climb"
    elif diff < 0:
        desc = "descent"
        diff = 0 - diff
 
    total_climb = 0
    total_desc = 0
    
    #calculate time - including additonal time for each climb and desc
    for x,p in enumerate(points[midpoint+1:]):
        d = points[x+midpoint] - p
        if d > 0:
            total_climb += d
        else:
            total_desc -= d
    
    time_distance = distance + float(total_climb)/1000 + float(total_desc)/1000
    speed = 20 #km/ph
    
    day = round(time/24,1)
    
    n_time = time_distance/speed
    h_time = human_travel(n_time)
    
    fnt = ImageFont.truetype('Raleway-Bold.ttf', 40)
    text = []
    

    if next:
    
        
        text.append(u"Day {0}: Arrived at {1}".format(day, here.name))
        text.append("{0} km and a {1} m {2}".format(distance,diff,desc))
        text.append(u"to {0}".format(next.name))
        text.append("Estimated Time: {0}".format(h_time))
        text.append("MPP: {1}m VE: {0}x".format(vertical_exaggeration,int(1/pixel_per_meter)))
        
    else:
        text.append(u"Day {0}: Arrived at {1}".format(day, here.name))
        text.append(u"Travelled: {0} km".format(round(total_distance,2)))
        text.append(u"Tour Completed")     
        
        
    text = "\n".join(text)
    


    
    #convert elevation points to local points
    
    rel_points = [convert(x) for x in points]
    
    coords = [(x,y) for x,y in enumerate(rel_points)]


    #draw land
    for x in range(0,length):
        this_point = coords[x]
        
        #draw bands of 100 meters on the land

        for y in range(int(mi),int(points[x]),100):
            ypoint = convert(y)
            draw.line(((x,ypoint),(x-1,ypoint)))
        
        #draw bandings on land
        for y in range(height,this_point[1],-5): 
            offset = x % 10
            if y - offset >= this_point[1]:
                draw.line(((x,y - offset),(x-1,y - offset)),fill="#D3D3D3")

    #draw points of interest (last, here, now)
    for x in poi:
        
        r = 8 # size of dot
        
        this_point = coords[x]
        xpoint = this_point[0]
        ypoint = this_point[1] -8
        
        
        red = (255,0,0)
        green = (0,255,0)
        if x == midpoint:
            draw.ellipse((xpoint-r, ypoint-r,xpoint+r,ypoint+r), fill=green)
        else:
            draw.ellipse((xpoint-r, ypoint-r,xpoint+r,ypoint+r), fill=red)    

    """
    draw captions and dropshadow
    """
    
    w, h = draw.textsize(text,font=fnt)
    text_x = (length/2) - w/2
    text_y = 20
    offset = 1
    
    
    
    draw.multiline_text((text_x-offset,text_y-offset),text,font=fnt,align="center",fill="black")
    draw.multiline_text((text_x+offset,text_y+offset),text,font=fnt,align="center",fill="black")
    draw.multiline_text((text_x+offset,text_y-offset),text,font=fnt,align="center",fill="black")
    draw.multiline_text((text_x+offset,text_y-offset),text,font=fnt,align="center",fill="black")
    draw.multiline_text((text_x,text_y),text,font=fnt,align="center")    
    

    return im, n_time


    
def three_points(obj1,obj2,obj3,running_time,running_distance):
    """
    creates an illustration with three POI (last point, here, next point). Expects Feature objects. 
    Key features of which are a 'name' property and a 'distance' method that when passed another 'feature'
    returns the distance calculated over the globe features are on. 
    """

    total_points = 1200 #samples to take (and so width of image)
    
    if obj3 == None: #last in chain
        distance1 = obj1.distance(obj2)[0]
        distance2 = distance1
        total = distance1 + distance2        
        """
        adjust our start and end to slightly overshoot (looks nicer)
        """
        extend = total * 0.05
        start_lat, start_long = obj2.overshoot(obj1,extend)
        end_lat, end_long = obj1.overshoot(obj2,distance1 + extend,short_percentage=1) # overshoot

    elif obj1 == None: #first in chain
        distance2 = obj2.distance(obj3)[0]
        distance1 = distance2
        total = distance1 + distance2           
        """
        adjust our start and end to slightly overshoot (looks nicer)
        """
        extend = total * 0.05
        start_lat, start_long = obj3.overshoot(obj2,distance2,short_percentage=1)#forces exactly as much distance
        end_lat, end_long = obj2.overshoot(obj3,extend)
    else:
        distance1 = obj1.distance(obj2)[0]
        distance2 = obj2.distance(obj3)[0]
        total = distance1 + distance2        
        """
        adjust our start and end to slightly overshoot (looks nicer)
        """
        extend = total * 0.05
        start_lat, start_long = obj2.overshoot(obj1,extend)
        end_lat, end_long = obj2.overshoot(obj3,extend)

    #generates paths between 1 and 2 and 2 and 3 (this appears as one continous line 
    #although in reality will often be at angles)
    
    set1 = get_intermediate_points(start_lat,
                                     start_long,
                                     obj2.center_lat,
                                     obj2.center_long,
                                     points=int((float(distance1)/total)*total_points)) #scale how much of the image is on each side
    

    set2 = get_intermediate_points(obj2.center_lat,
                                     obj2.center_long,
                                     end_lat,
                                     end_long,
                                     points=int((float(distance2)/total)*total_points))
    
    
    all_points = set1 + set2[1:]
    
    """
    find points on our path closest to the original ones - so we can put markers on them
    """
    
    radius = obj2.target.radius    
    def sort_points(v,target_lat,target_long):
        lat,lng = v[1]
        return lat_long_distance(target_lat,target_long,lat,lng,radius)
        
    points_in_order = [x for x in enumerate(all_points)]
    
    poi = []
    for o in [obj1,obj2,obj3]:
        if o:
            points_in_order.sort(key=lambda x: x[0]) #reset
            
            if o == obj1:
                valid_range = points_in_order[:len(points_in_order)/2] #if doubling back - forces it on the left
            else:
                valid_range = points_in_order
            valid_range.sort(key=lambda x: sort_points(x,o.center_lat,o.center_long))
            poi.append(valid_range[0][0])
    
    ele = get_moon_elevation(all_points)
    im, time = illustrate(ele, poi=poi,objs=[obj1,obj2,obj3],time=running_time,total_distance=running_distance)
    
    return im,time,distance2
    

if __name__ == "__main__":
    print get_moon_elevation([(26.58,16.43)]) #test points
    print get_moon_elevation([(25.8,3.8)])
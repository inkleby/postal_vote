# -*- coding: utf-8 -*-
import math

def calculate_initial_compass_bearing(pointA, pointB):
    """
    https://gist.github.com/jeromer/2005586
    
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def project_lat_long(lat,lng,radius,bearing,distance):
        #http://gis.stackexchange.com/questions/129611/distance-with-bearing-calculation-not-working
        # convert Latitude and Longitude
        # into radians for calculation
        d = distance
        R = radius
        brng = math.radians(bearing)
    
        lat1 = math.radians(lat) #Current lat point converted to radians
        lon1 = math.radians(lng) #Current long point converted to radians
        
        lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
             math.cos(lat1)*math.sin(d/R)*math.cos(brng))
        
        lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                     math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
        
        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
                
        return lat2,lon2
    
def short_overshoot(y1,x1,y2,x2,percent=0.05):
    """
    for short distances fudge it
    """
    diffx = x2-x1
    diffy = y2-y1
    
    newx = x1 + (diffx * (1 + percent))
    newy = y1 + (diffy * (1 + percent))
    
    return newy,newx
    
    
def lat_long_distance(y1,x1,y2,x2,radius):
        """
        distance between two lat longs
        """
        size_of_degree = 2*math.pi*radius/360 #on target planet

        rx1 = math.radians(x1)
        ry1 = math.radians(y1)
        rx2 = math.radians(x2)
        ry2 = math.radians(y2)
        
        if rx1 == rx2 and ry1 == ry2:
            return 0
        
        angle1 = math.acos(math.sin(rx1) * math.sin(rx2) \
                 + math.cos(rx1) * math.cos(rx2) * math.cos(ry1 - ry2))
        
        angle1 = math.degrees(angle1)
        
        distance = size_of_degree * angle1
        
        return distance
    
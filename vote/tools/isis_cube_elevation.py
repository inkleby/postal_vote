'''

Can read ISISCube and return point information

Designed to read the moon elevation cab and return elevation data

'''

import gdal
from gdalconst import GA_ReadOnly
import struct

class IsisCube(object):
    """
    open a cube file to extract elevation locations from it
    """
    def __init__(self,filename,conversion = lambda x : x):
        """
        accepts a filename and a lambda conversion - if points need to be adjusted
        before being returned (e.g. if points are exaggerated by 2 and have an offset of 10000 (lambda x : (x * 0.5) + 10000)
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
        if lat != lat or lng != lng: #detect NaN
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

    


if __name__ == "__main__":   
    # source http://astrogeology.usgs.gov/search/details/Moon/LRO/LOLA/Lunar_LRO_LOLA_Global_LDEM_118m_Mar2014/cub
    lunar_cab = "E:\\lunar.cub" #sub your location here
    
    #conversion_lambda = lambda x: (x * 0.5) + 1737400 #for measurement from center of moon, not 'average'
    conversion_lambda = lambda x: (x * 0.5) #LRO data is adjusted by 0.5
    
    
    i = IsisCube(lunar_cab, conversion = conversion_lambda)
    
    print i.point(0.67408, 23.47297)

'''
Image Tiler - given an image will produce tiles that can be used in a google maps tileset.

Key function - process_image - accepts a image path location and produces tiles in a "\tiles" folder at that location. 

'''
from PIL import Image
import math
import os

tile_size = 256
image_format = "{0}_{1}_{2}.png"

def proportional_resize(img,new_width):
    """
    resizes based just on width (if your image is tall rather than wide you'll have to adjust this)
    """
    width,height = img.size
    
    resize_height = int((float(height)/float(width)) * new_width)
    
    return img.resize((int(new_width),resize_height),Image.ANTIALIAS)


def resize_and_save(img,save_loc,size=tile_size):
    """
    makes the image a 256 square - padding with black at the bottom
    """
    
    reduced = proportional_resize(img,size)

    width,height = reduced.size
    if width <> height:
        pad = Image.new(img.mode, (size,size))
        pad.paste(reduced, (0,0,width,height))
        reduced = pad
        
    print "saving {0}".format(save_loc)
    reduced.save(save_loc)


def get_initial_image(img):
    
    """
    resizes images downwards to the max zoom level - reduced reduced
    and the zoom level
    """
    width, height = img.size
    max_size = -1
    for x in range(0,8): #max depth of 7 allowed
        pixels = tile_size * math.pow(2,x)
        if pixels > width:
            break
        max_size += 1
        
    print "determined {0} is maximum zoom level - resizing source image to max".format(max_size)
    safe_width = tile_size * math.pow(2,x)
    resized = proportional_resize(img,safe_width)
    print "done"
    return resized,max_size

def create_tiles(img,zoom_level,image_save_path):
    """
    slices the image up into tiles at this zoom level
    """
    number_of_tiles = int(math.pow(2,zoom_level))
    print "creating level {0} tiles".format(zoom_level)
    width,height = img.size
    width_slice = width/number_of_tiles
    height_count = int(math.ceil(float(height)/float(width) * number_of_tiles))
    
    for w in range(0,number_of_tiles):
        start_x = w * width_slice
        end_x = start_x + width_slice - 1
        for h in range(0,height_count):
            start_y = h * width_slice
            end_y = start_y + width_slice - 1
            if end_y > height:
                end_y = height
            
            img_slice = img.crop((start_x, start_y, end_x, end_y))
            filename = image_format.format(zoom_level,w,h)
            path = os.path.join(image_save_path,filename)
            resize_and_save(img_slice,path)
            


def process_image(image_path):
    """
    given an image file will slice it into tiles to the maximum level allowed
    and dump in that file location
    """
    print "opening image file"
    img = Image.open(image_path)
    
    width,height = img.size
    
    resize_ratio = float(height)/float(width)*255
    print resize_ratio
    
    tile_path = os.path.join(os.path.dirname(image_path),"tiles")
    if not os.path.exists(tile_path):
        os.makedirs(tile_path)
    
    img, zoom_level = get_initial_image(img)
    
    for x in range(0,zoom_level+1):
        create_tiles(img,x,tile_path)


if __name__ == "__main__":
    process_image('E:\\display_maps\\maps\\callisto\\callisto_simp_1km.jpg')
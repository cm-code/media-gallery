# media-gallery 1.0
A simple, filesystem-derived gallery that works with mod_python.  

# Requirements:

python >= 2.7.x  
argparse >= 1.2.x   
mod_python >= 3.4.3  

A modern release of:  
Python Imaging Library   
ImageMagick that supports JPEG2000 & Fuji RAW (for thumbnail generation)

# Configuration:

Settings are in img_gallery.conf as follows:

Base path (where the gallery starts on disk):

For example, a gallery starting in path /var/galleries:

basepath=/var/galleries

Web path (where the gallery starts as seen from the user accessing the site):

For example, a gallery starting in a remote server's /gallery directory:

webpath=/gallery

#  Thumbnail Generation:

If you wish to generate them:  
By default, thumbnails are not generated. To do so, run:  
    python img_dwalk.py [path] 
 
Where [path] is the base path of your galleries on disk.  Anything below [path] will be scanned and a thumbnail will be generated to replace the default placeholder.  


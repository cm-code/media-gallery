# media-gallery
A simple, filesystem-derived gallery that works with mod_python.  

# Requirements:

python >= 2.7.x  
argparse >= 1.2.x   
mod_python >= 3.4.3  

A modern release of:  
Python Imaging Library   
ImageMagick that supports JPEG2000 & Fuji RAW    

# Configuration:

Settings are in img_gallery.conf as follows:

Base path (where the gallery starts on disk):

For example, a gallery starting in path /var/galleries:

basepath=/var/galleries

Web path (where the gallery starts as seen from the user accessing the site):

For example, a gallery starting in a remote server's /gallery directory:

webpath=/gallery



# TODO:

Add gallery generation script.

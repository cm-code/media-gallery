#
#
#    image-gallery 
#    2010-2016+, Charles Monett
#     
#    
#
#
#


from mod_python import * 
from PIL import Image, ExifTags
import fnmatch, re
import argparse as ap
import os,sys


def index(req):
	try:
		 list_dir(req,s_subdir)
	except:
		 s_subdir="/"
		 list_dir(req,s_subdir)
	return 

def about_app(req):
	req.content_type = 'text/html'
	req.write(_do_header())
	l_abt_header = []
	l_abt_header.append('<div class="topbox">\n')
        l_abt_header.append('<div class="maintextb">About Media Gallery</div><br>\n')
        l_abt_header.append('<div class="maintexta">A media gallery application.<br>2010-2016, Charles Monett.</div><br>\n')
        l_abt_header.append('</div>\n')
	req.write(''.join(l_abt_header))
	return ""

def _error_msg(req):
        req.content_type = 'text/html'
        req.write(_do_header())
        l_abt_header = []
        l_abt_header.append('<div class="topbox">\n')
        l_abt_header.append('<div class="maintextb">Configuration Error</div><br>\n')
        l_abt_header.append('<div class="maintexta">Please supply a valid img_gallery.conf file.<br>See documentation for syntax.</div><br>\n')
        l_abt_header.append('</div>\n')
        req.write(''.join(l_abt_header))
        return ""


def _prune_list(Lx,Ly,str):
	for x, d_tuple in enumerate(Lx):
		Lx[x] = Lx[x].replace(str, '')
	Lz = list(set(Ly).difference(set(Lx)))
	return Lz

def _strip_char(L, str):
	for x, d_tuple in enumerate(L):
		L[x] = L[x].replace(str,'')
	return L

def _swap_char(L, str_a, str_b):
	for x, d_tuple in enumerate(L):
		L[x] = L[x].replace(str_a,str_b)
	return L




def _bad_metachars(L):
	# grab an empty list, populate it
	L.append("..\\")
	L.append("../")
	L.append("..")
	L.append("...")
	L.append("\"")
	L.append("\'")
	L.append("\*")
	L.append("\=")
	L.append("\\")
	L.append("<")
	L.append(">")
	#L.append("%3F")
	#L.append("%")
	L.append("%u")
	L.append("%s")
	L.append("%r")
	L.append("%a")
	L.append("%x")
	#L.append("#")
	L.append(":")
	L.append("=")
	L.append("@")
	#L.append("&")
	L.append("*")
	L.append("?")
 		
	return 
	
def _do_header():
	l_header = []
        l_header.append('<html xmlns="http://www.w3.org/1999/xhtml">\n')
        l_header.append('<head>\n')
        l_header.append('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
        l_header.append('<title>Media Gallery</title>\n')
        l_header.append('<link href="/ig-css/gallery_ig.css" rel="stylesheet" type="text/css" />\n')
        l_header.append('<link href="/ig-css/gallery_aux.css" rel="stylesheet" type="text/css" />\n')
        l_header.append('<link href="/ig-css/gallery_assets.css" rel="stylesheet" type="text/css" />\n')
        l_header.append('<link href="/ig-css/gallery_ui.css" rel="stylesheet" type="text/css" />\n')
        l_header.append('\n')
        l_header.append('</head>\n')
        l_header.append('<body>\n')
        l_header.append('<br />\n')
        l_header.append('<div class="linkbar c3">\n')
        l_header.append('<div class="horgradbw c2c"></div>\n')
        l_header.append('</div>\n')
	return(''.join(l_header))

def _do_truepath(rt_file):
	t_path = os.path.realpath(rt_file)
	tl_path = os.path.split(t_path)
 	return tl_path	


def list_dir(req,s_subdir):
  	
        s_conf = ap.Namespace()
	
	# actual path 
        l_path = _do_truepath(__file__)
        s_path = l_path[0]
	# script name
	s_script = str(os.path.basename(__file__)) 

	# filename
	s_file = "/img_gallery.conf"

        # Cut through symlinks
        l_confpath = [s_path, s_file]
        s_config = "".join(l_confpath)

        # read settings
        with open(s_config) as f:
                for line in f:
                        s_settings = line.strip().split('=', 1)
                        setattr(s_conf,s_settings[0],s_settings[1])

	# Configure from file.  If missing, error out.	
	#try:
	s_basepath = s_conf.basepath
 	s_webpath = s_conf.webpath
	#except:
	#	_error_msg(req)
	#	return
	
	#root directory test	
        if s_subdir == "/":
		s_subdir = ""
	elif len(s_subdir) == 0:
		s_subdir = ""
	elif len(s_subdir) != 0 and s_subdir[-1] != "/":
		s_subdir="%(s_subdir)s" % locals()	

	#set content type
	req.content_type = 'text/html'

 	# write header for main 	
	req.write(_do_header())

	#list of images, sorted
	# Remove bad characters from user input
	l_bad_chars = []
	_bad_metachars(l_bad_chars)
	#req.write(''.join(l_bad_chars)) #enable to see replaced chars
	for x, d_tuple in enumerate(l_bad_chars):
		s_subdir = s_subdir.replace(l_bad_chars[x],'')
	
	# Gallery name
	s_gallery_name = s_subdir #.replace('/','',1)
	s_gallery_name = (s_gallery_name[:125] + "&hellip;") if len(s_gallery_name) > 75 else s_gallery_name
        # assemble clean path elements	
	l_path = []
	l_path.append(s_basepath)
	l_path.append(s_subdir)
	s_namepath = ''.join(l_path)        
 
	
	
	try:
		s_path = "%(s_basepath)s%(s_subdir)s" % locals()
		s_wpath = "%(s_webpath)s%(s_subdir)s" % locals() 	
		l_web_images = os.listdir(s_path)
		l_thumbnail = fnmatch.filter(l_web_images, "tn_*.*")
		l_web_images = _prune_list(l_thumbnail, l_web_images, s_namepath)
	except:
		s_gallery_name = ""
		s_namepath = s_basepath
		s_subdir = ""
		s_path = "%(s_basepath)s%(s_subdir)s" % locals()
		s_wpath = "%(s_webpath)s%(s_subdir)s" % locals() 
		l_web_images = os.listdir(s_path)
		l_thumbnail = fnmatch.filter(l_web_images, "tn_*.*")
                l_web_images = _prune_list(l_thumbnail, l_web_images, s_namepath)                


	# Remove thumbnails
	
	# Remove scripts, flash, non-image media		
	r_unwanted = [ "jp2", "php", "phps", "py", "pl", "sh", "htm", "css", "swf", "tif", "meta", "torrent", "txt", "diz", "nfo" ]
        
	for rr_thumbnail in r_unwanted:
		 rs_thumbnail = "*.",rr_thumbnail  
		 s_thumbnail = fnmatch.filter(l_web_images, rs_thumbnail) 
                 l_web_images = _prune_list(s_thumbnail, l_web_images, s_namepath)
 	
	# Sort media 		
	l_web_images.sort()

	# Parameters inside
	i_x = len(l_web_images) # amount of items
	i_y = 0  # completed rows
	i_zi = 1  # initial position in current (incomplete row)
	i_zf = 4  # final   position in current row (column width)
	i_mult = 240 #pixel height multiplier
	i_offset = 160 #height offset

	s_ypos = str(i_y + i_offset)
	s_ycap = str(i_y*200 + 160)
	s_ybar = str(i_y + i_offset - 20)

	# div elements
	s_divgen = '<div>'
	s_div1 = '<div class="outer">'
	s_div2 = '<div class="image_holder">'
	s_div3 = '<div class="image_tx" style="width:200px; height:220px; background-color:#ffffff; border-style:solid; border-width:1px; overflow:hidden; word-wrap:break-word; word-break:break-all;">'
	s_div4 = '<div class="caption_tx" style="width:198px; height:60px; left:1px; position:absolute; overflow:hidden; top:%(s_ycap)spx; background-color:#ffffff; text-align:center; font-family:Tahoma,Verdana,Sans,Helvetica; font-size:11px;">' % locals()
	s_divend = '</div>'
	
	# string for subdir
	l_url_subdir = []
	l_url_subdir.append(s_script)
	l_url_subdir.append("/list_dir?s_subdir=")
	s_url_subdir = ''.join(l_url_subdir)
	s_url_subdir = '/img_gallery.py/list_dir?s_subdir='

	
	# outer div
	l_html_list = []	
	l_html_list.append('<div class="image_header_bar"><div class="image_header_text">Gallery: %(s_gallery_name)s <br/> Items:%(i_x)i items</div></div>' % locals())
	l_html_list.append(s_div1)
	
	#
	# main list loop
	#

 	# l_html_list.append('<!-- Script Invoked: %(s_script)s -->' % locals() ) # Debug Use
	
	while i_zf * i_y + i_zi <= i_x:
		i_pos = i_zf * i_y + i_zi - 1 # our position in the list
		s_pos = str(i_pos)	      # string rendering of our position	
		s_file = l_web_images[i_pos]  # list entry
		
		# Web-ready entries
		s_tn_link = '%(s_webpath)s%(s_subdir)stn_%(s_file)s' % locals()
		s_fi_link = '%(s_webpath)s%(s_subdir)s%(s_file)s' % locals()						
		
		# Filesystem entries 
		s_fs_link = '%(s_path)s%(s_subdir)s%(s_file)s' % locals()
		s_ft_link = '%(s_path)s%(s_subdir)stn_%(s_file)s' % locals()	
	
		if s_subdir != "":
			s_fs_link = '%(s_path)s%(s_file)s' % locals()
			s_ft_link = '%(s_path)stn_%(s_file)s' % locals()
		
		#req.write('<!-- %(s_fs_link)s %(s_ft_link)s -->\n' % locals())
		
		# Test to see if the file is a directory, replace:
		# * Image with directory image
		# * Entry with subdir link
		if os.path.isdir(s_fs_link) == True and len(s_subdir) != 0:
			#req.write('<!-- dir-marker %(s_file)s -->\n' % locals() )
			#Return a generic directory image.
			s_tn_link = '/ig-images/i_folder.jpg' % locals()
			s_fi_link = '%(s_url_subdir)s%(s_subdir)s/%(s_file)s/' % locals()
			req.write(' <!-- url_subdir: %(s_url_subdir)s subdir: %(s_subdir)s file: %(s_file)s -->' % locals() )
		elif os.path.isdir(s_fs_link) == True:
			#req.write('<!-- dir-marker %(s_file)s -->\n' % locals() )
			#Return a generic directory image.
			s_tn_link = '/ig-images/i_folder.jpg' % locals()
			s_fi_link = '%(s_url_subdir)s%(s_file)s/' % locals()
			req.write(' <!-- url_subdir: %(s_url_subdir)s file: %(s_file)s -->' % locals() )
		elif os.path.exists(s_ft_link) == False:
			s_tn_link = '/ig-images/i_nothumb.jpg' % locals()
	 	
		# Clean up path
		s_fi_link = s_fi_link.replace('//','/')	
	 	s_fi_link = s_fi_link.replace(' ','%20')	



		#endif
		# Output list items.
		if i_zi >= i_zf: # our position is last in column but not in list
   			# pull data out and print it
			s_cssentry = str(i_zi)
			s_position = str(i_zi * 200 - 1 - 70)
			s_ypos = str((i_y * i_mult)+i_offset)
	    		s_ycap = str(i_y * 200 + 170)
	               
			l_html_list.append('<div class="group%(s_cssentry)sx%(s_ypos)sy" style="position:absolute; width:200px; height:200px; top:%(s_ypos)spx; left:%(s_position)spx;">' % locals())	
			l_html_list.append(s_div3)
			l_html_list.append(s_div2)
			l_html_list.append('<a href="%(s_fi_link)s"><img src="%(s_tn_link)s" alt="%(s_file)s" /></a>' % locals())
			l_html_list.append(s_divend)
			l_html_list.append(s_divend)
			l_html_list.append(s_div4)
			l_html_list.append('<a href="%(s_fi_link)s">%(s_file)s</a>' % locals())
			l_html_list.append(s_divend)
			l_html_list.append(s_divend) # terminate entry 
					

	                # reset position and incremement 
	                i_zi = 1  # reset position 
	                i_y += 1  # increment completed row
        
		elif i_zi == 1: # our position is first in column
			# pull data out
					
		        s_cssentry = str(i_zi)
			s_position = str(i_zi * 200 + 1 - 70)
			s_ypos = str((i_y * i_mult)+i_offset)
			s_ycap = str(i_y * 200 + 170)

		        l_html_list.append('<div class="group%(s_cssentry)sx%(s_ypos)sy" style="position:absolute; width:200px; height:200px; top:%(s_ypos)spx; left:%(s_position)spx;">' % locals())
        	        l_html_list.append(s_div3)
	                l_html_list.append(s_div2)
			l_html_list.append('<a href="%(s_fi_link)s"><img src="%(s_tn_link)s" alt="%(s_file)s" /></a>' % locals())
			l_html_list.append(s_divend)
        	        l_html_list.append(s_divend)
	                l_html_list.append(s_div4)
	                l_html_list.append('<a href="%(s_fi_link)s">%(s_file)s</a>' % locals())
	                l_html_list.append(s_divend)
			l_html_list.append(s_divend)

			i_zi += 1 #increment position

		else: 
        	        # pull data out and print it  
			s_cssentry = str(i_zi)
			s_position = str(i_zi * 200 - 70)
			s_ypos = str((i_y * i_mult)+i_offset)
	    		s_ycap = str(i_y * 200 + 170)

			# detect directories here.
			i_detect = os.path.isdir(s_file)
			

			l_html_list.append('<div class="group%(s_cssentry)sx%(s_ypos)sy" style="position:absolute; width:200px; height:200px; top:%(s_ypos)spx; left:%(s_position)spx;">' % locals())
			l_html_list.append(s_div3)
			l_html_list.append(s_div2)
			l_html_list.append('<a href="%(s_fi_link)s"><img src="%(s_tn_link)s" alt="%(s_file)s" /></a>' % locals())
			l_html_list.append(s_divend)
	 		l_html_list.append(s_divend)
			l_html_list.append(s_div4)
			l_html_list.append('<a href="%(s_fi_link)s">%(s_file)s</a>' % locals())
	                l_html_list.append(s_divend)
			l_html_list.append(s_divend)
                
			# increment position
	                i_zi += 1 #increment position
	l_html_list.append(s_divend)
	
	req.write('\n'.join(l_html_list))
	req.write('</body></html>')

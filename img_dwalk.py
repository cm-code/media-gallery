#!/usr/local/bin/python

#
#
#  Companion Script to media-gallery
#  2010-2016+, Charles Monett
#  
#  Purpose: Generates thumbnails for images in a given directory tree
#  Does limited conversion 
#  Syntax: img_dwalk.py [path] 
#   
#

import os, sys
import subprocess
import fnmatch
import datetime
from PIL import Image, ExifTags
s_totals = [0,0,0,0]


class filetree(object):
	
	def __init__(self,rfpath,rfmask):
		self.rfpath = rfpath
		self.rfmask = rfmask


# change_extension(filename, new extension)
# 
def change_extension(s_filename,dst_ext):
	# Check length of data wishing to be truncated.   
	# If it is less than the length of the string, truncate, reassemble, and return new filename.
	# If it exceeds the length of the string, return "ERROR".
	lr = 0
	if len(s_filename) > len(dst_ext): 
		sl_list = [s_filename[0:-len(dst_ext)],dst_ext]
	  	for num in xrange(lr):
			sl_list.append(`num`) 
		sl_entry = ''.join(sl_list)
		return sl_entry
	else:
	        return "ERROR"	
	

def dirwalk(rfpath, rfmask):
	lc = 0
	ld = 0
	le = 0
	img_count=0
	img_total=0 
	img_error=0
	for dirpath, dirs, files in os.walk(rfpath):
		for f in sorted(fnmatch.filter(files, rfmask)):
			
			# join entries for path of filename
			f_list = [dirpath,"/", f]	
			for num in xrange(lc):
				f_list.append(`num`)			
			file_entry = ''.join(f_list)
		
		        # If the file is in need of conversion, do so before everything else.
                        # After conversion, point to the new file and resume processing.
			# 
			# Conversions performed by: ImageMagick	
			# Conversions currently supported:  JPEG2000, Fuji RAW	
                        # Conversion destination: JPEG
			if rfmask in ("*.jp2", "*.JP2", "*.raf", "*.RAF"):
				print "[C] Changing %s to %s " %(f,change_extension(f,"jpg"))
                                fr = change_extension(file_entry,"jpg")
                                fc = change_extension(f,"jpg")
			        print file_entry, fr	
				subprocess.call(["convert",file_entry,fr])
                                
				file_entry = fr
				f = fc	
			
			# test to see if there is a thumbnail		
	       		tl_list = [dirpath,"/tn_",f]
			for num in xrange(le):
				tl_list.append(`num`)
			t_entry = ''.join(tl_list)
			
			# attempt to open the thumbnail.
			# if it doesnt exist, set err_io to thumb
			if f[:3] != "tn_":
				try:
					with open(t_entry) as ft:
						err_io = "nothumb"
						print "[E] %s exists as a thumbnail.  Not creating one." %(t_entry)
						ft.close	
                        	except IOError as e:
					err_io = "thumb"	
			 		print "[I] %s does not have a thumbnail.  Will create tn_%s." %(f,f)
				img_total += 1
			# test to see if this is a thumbnail.
			# if it is not, then process it.
			# if it is, then print a message and skip it.	
			if f[:3] != "tn_" and err_io == "thumb":
				#assemble pieces
				t_list = [dirpath,"/tn_",f]
				for num in xrange(ld):
					t_entry.append(`num`)
				thumb_entry = ''.join(t_list) 
					
				#resize and save as tn_[filename]
				try:
					image_entry = Image.open(file_entry)
					image_save = image_entry.resize((150,150), Image.ANTIALIAS)
					image_save.save(thumb_entry)
				
					# record saved image, increment
					print "[+] %s has been saved as tn_%s" % (f,f)
					img_count += 1
			 		pass	
				except:
					print "[E] Error handling %s" % f
					img_error += 1
				#else:
				#	# record thumbnail error, increment
				#	print "[E] %s is a thumbnail, not making a copy" % (f)
	# return with totals
	img_diff = img_count + img_error
	dl_totals = [img_count,img_error,img_diff,img_total]
	return dl_totals 

def do_report(l_totals):
 	# provide report of images
	  
	print "=" * 50
	print "Images processed    : %i" % l_totals[0]
	print "Images in error     : %i" % l_totals[1]
	print "Images present      : %i" % l_totals[2]
 	print "Items processed     : %i" % l_totals[3]
	print "=" * 50	

#	
# actions
#

# declare list of formats then process them through that path 
fmt_list = ["*.jpeg", "*.JPEG","*.jpg", "*.JPG","*.jp2","*.png","*.PNG","*.gif","*.GIF"]
for fmt in fmt_list:
	try:
		l_dirpath = [ sys.argv[1], "/"] 
		rl_path = ''.join(l_dirpath)
		print rl_path
		imagetree = filetree(rl_path, fmt)
	except:
		print "Usage:"
		print "img_dwalk.py [valid path]"
		sys.exit(1)
	# walk tree with extension
	r_totals = dirwalk(imagetree.rfpath, imagetree.rfmask)
	#do_report(r_totals)	
	# increment totals  
	s_totals[0] = s_totals[0] + r_totals[0]
	s_totals[1] = s_totals[1] + r_totals[1]
	s_totals[2] = s_totals[2] + r_totals[2]
	s_totals[3] = s_totals[3] + r_totals[3]
do_report(s_totals)

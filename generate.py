import sys
from PIL import Image
import os

# ****** FUNCTIONS ******
def print_info():
	print("Usage: " + str(sys.argv[0]) + " source-directory output-directory")
	print("\nScan a directory for images and generate thumbnails and an html document listing them.")
	print("\nsource-directory: the directory the images are stored in.")
	print("output-directory: where the index and thumbnails will be stored.\n")
	
def generate_thumbnail(source_dir, target_dir, filename):
	try:
		im = Image.open(source_dir + "/" + filename)
		im.thumbnail((256, 256))
		im.save(target_dir + "/thumbnails/" + filename)
		im.close()
	except Exception as e:
		print(str(e))
	
# ****** HELP COMMAND ******
if sys.argv[1] == "-h" or sys.argv[1] == "--help":
	print_info()
	
# ****** NORMAL EXECUTION ******
else:
	# Stops here if not enough args
	if not len(sys.argv) > 2:
		print("Error: not enough arguments.\n")
		print_info()
		
	#Stop here if invalid source directory
	elif not os.path.isdir(sys.argv[1]):
		print("Error: invalid source directory.\n")
		print_info()
	
	#Stop here if invalid output directory
	elif not os.path.isdir(sys.argv[2]):
		print("Error: invalid output directory.\n")
		print_info()
		
	#Both dirs exist
	else:
		#make the thumbnail subfolder if it doesn't already exist
		if not os.path.isdir(sys.argv[2] + "/thumbnails/"):
			os.mkdir(sys.argv[2] + "/thumbnails/")
		
		#scan thumbnails to make sure the original files haven't been removed.
		thumb_files = os.listdir(sys.argv[2] + "/thumbnails")
		for name in thumb_files:
			#original file is gone
			if not os.path.isfile(sys.argv[1] + "/" + name):
				os.remove(sys.argv[2] + "/thumbnails/" + name)
		
		#get list of files
		files = os.listdir(sys.argv[1])
		
		for name in files:
			print("\nProcessing " + name)
			#thumbnail already exists
			if os.path.isfile(sys.argv[2] + "/thumbnails/" + name):
				#get modified date of both image and thumbnail to determine if the thumbnail is out of date.
				orig_date = os.path.getmtime(sys.argv[1] + "/" + name)
				thumb_date = os.path.getmtime(sys.argv[2] + "/thumbnails/" + name)
				# orig_date will be greater than thumb_date if it has been modified
				if orig_date > thumb_date:
					generate_thumbnail(sys.argv[1], sys.argv[2], name)
			else:
				generate_thumbnail(sys.argv[1], sys.argv[2], name)				
		
	

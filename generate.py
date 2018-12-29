import sys
from PIL import Image
import os

# ****** FUNCTIONS ******
def print_info():
	print("Usage: " + str(sys.argv[0]) + " source-directory output-directory html-directory insertion-target final-output-dir")
	print("\nScan a directory for images and generate thumbnails and an html document listing them.")
	print("\nsource-directory: the directory the images are stored in.")
	print("\noutput-directory: where the index and thumbnails will be stored.")
	print("\nhtml-directory: the directory the generated html will be saved in.")
	print("\ninsertion-target: the html file on the server that should have the generated html inserted into it.")
	print("\nfinal-output-dir: the directory of file that will be generated at the end.\n")
	
def generate_thumbnail(source_dir, output_dir, filename):
	try:
		im = Image.open(source_dir + filename)
		im.thumbnail((256, 256))
		im.save(output_dir + filename)
		im.close()
	except Exception as e:
		print(str(e))
	
# ****** HELP COMMAND ******
if sys.argv[1] == "-h" or sys.argv[1] == "--help":
	print_info()
	
# ****** NORMAL EXECUTION ******
else:
	if not len(sys.argv) > 5:
		print("Error: not enough arguments.\n")
		print_info()
		
	elif not os.path.isdir(sys.argv[1]):
		print("Error: invalid source-directory.\n")
		print_info()
	
	elif not os.path.isdir(sys.argv[2]):
		print("Error: invalid output-directory.\n")
		print_info()
		
	elif not os.path.isdir(sys.argv[3]):
		print("Error: invalid html-directory.\n")
		print_info()
		
	elif not os.path.isfile(sys.argv[4]):
		print("Error: invalid insertion-target.\n")
		print_info()
		
	elif not os.path.isdir(sys.argv[5]):
		print("Error: invalid final-output-dir.\n")
		print_info()

	#all dirs exist
	else:
		source_dir = sys.argv[1]
		output_dir = sys.argv[2]
		html_dir = sys.argv[3]
		insertion_target = sys.argv[4]
		final_dir = sys.argv[5]
		
		# this makes processing more convenient
		if not source_dir.endswith('/'):
			source_dir = source_dir + "/"
		if not output_dir.endswith('/'):
			output_dir = output_dir + "/"
		if not html_dir.endswith('/'):
			html_dir = html_dir + "/"
		
		# track whether any actual changes happened.
		modified=False
		
		#scan thumbnails to make sure the original files haven't been removed.
		thumb_files = os.listdir(output_dir)
		for name in thumb_files:
			#original file is gone
			if not os.path.isfile(source_dir + name):
				os.remove(output_dir + name)
				modified = True
		
		#get list of files
		files = os.listdir(source_dir)

		#Parse all image files
		for name in files:
			# make sure it's not a directory or something, this isn't recursive
			if os.path.isfile(source_dir + name):
				#thumbnail already exists
				if os.path.isfile(output_dir + name):
					#get modified date of both image and thumbnail to determine if the thumbnail is out of date.
					orig_date = os.path.getmtime(source_dir + name)
					thumb_date = os.path.getmtime(output_dir + name)
					# orig_date will be greater than thumb_date if it has been modified
					if orig_date > thumb_date:
						generate_thumbnail(source_dir, output_dir, name)
						modified = True
				else:
					generate_thumbnail(source_dir, output_dir, name)
					modified = True		
		
		#Thumbnails generated: make the html
		#TODO: make these values not hardcoded.
		html_filename = html_dir + "output.html"
		if modified or not os.path.isfile(html_filename):
			if os.path.isfile(html_filename):
				os.remove(html_filename)
			with open(html_filename, "a+") as html_file:
				for name in files:
					html_file.write('<div class="info-box">\
									\n\t<a href="https://files.voidlurker.net/' + name + '">\
									\n\t\t<img src="https://files.voidlurker.net/thumbnails/' + name + '"/><p>' + name + '</p>\
									\n\t</a>\
									\n</div>\n')
			with open(html_filename, "r") as html_file:
				with open(insertion_target, "r") as insertion_file:
					replacement_string = insertion_file.read()
				replacement_string = replacement_string.replace("REPLACE_ME", html_file.read())
				with open(final_dir + "/gallery.html", "w+") as final_file:
					final_file.write(replacement_string)
					
					
					
					
					
					
					
					
					
					
				
	

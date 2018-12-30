import sys
from PIL import Image
import os
import configparser

# ****** FUNCTIONS ******
def print_info():
    print("Usage: " + str(sys.argv[0]) + "[-h --help][--generate-config]")
    print("\nScan a directory for images and generate thumbnails and an html document listing them.")
    print("\n    --generate-config: create a 'config.ini' in the active directory with empty values.")

    
def generate_thumbnail(source_dir, output_dir, filename):
    try:
        im = Image.open(source_dir + filename)
        im.thumbnail((256, 256))
        im.save(output_dir + filename)
        im.close()
    except Exception as e:
        print(str(e))
    
config = configparser.ConfigParser()

running = True
# ****** HELP COMMAND ******
for arg in sys.argv:
    if arg == "-h" or arg == "--help":
        print_info()
        running = False
        break

    elif arg == "--generate-config":
        running = False
        print("Generating default configuration at 'config.ini'")
        config["PATHS"] = { "source-dir": "None",
                            "output-dir": "None",
                            "html-dir": "None",
                            "template-file": "None",
                            "gen-file": "None" }
        
        with open("config.ini", "w+") as config_file:
            config.write(config_file)
        

# ****** NORMAL EXECUTION ******
if running:
    
    config.read("config.ini")

    source_dir = config["PATHS"]["source-dir"]
    if not os.path.isdir(source_dir):
        sys.exit("Invalid source-directory")
    
    output_dir = config["PATHS"]["output-dir"]
    if not os.path.isdir(output_dir):
        sys.exit("Invalid output-directory")
        
    html_dir = config["PATHS"]["html-dir"]
    if not os.path.isdir(html_dir):
        sys.exit("Invalid html-dir")
    
    template_filename = config["PATHS"]["template-file"]
    try:
        template_file = open(template_filename, "r")
        template_file.close()
    except:
        sys.exit("Invalid template-file")
        
    gen_filename = config["PATHS"]["gen-file"]
    try:
        gen_file = open(gen_filename, "w+")
        gen_file.close()
    except:
        sys.exit("Invalid template-file")
    
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
            print("Deleting thumbnail for removed file: " + name)
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
                    print("Generating thumbnail for updated file: " + name)
                    generate_thumbnail(source_dir, output_dir, name)
                    modified = True
                else:
                    print(name + " is up to date")
            else:
                print("Generating thumbnail for new file: " + name)
                generate_thumbnail(source_dir, output_dir, name)
                modified = True        
    
    #Thumbnails generated: make the html
    #TODO: make these values not hardcoded.
    html_filename = html_dir + "output.html"
    if modified or not os.path.isfile(html_filename):
        if os.path.isfile(html_filename):
            os.remove(html_filename)
        with open(html_filename, "a+") as html_file:
        
            # create a dict using modification date as key, to sort by
            sorted_namelist = {}
            for name in files:
                sorted_namelist[os.path.getmtime(source_dir + name)] = name;
            
            
            for key in sorted(sorted_namelist, reverse=True):
                name = sorted_namelist[key]
                html_file.write('<div class="info-box">\
                                \n\t<a href="https://files.voidlurker.net/images/' + name + '">\
                                \n\t\t<img src="https://files.voidlurker.net/thumbnails/' + name + '"/><p>' + name + '</p>\
                                \n\t</a>\
                                \n</div>\n')
                print("Wrote " + name + " to " + html_filename)
        with open(html_filename, "r") as html_file:
            with open(template_filename, "r") as template_file:
                replacement_string = template_file.read()
            replacement_string = replacement_string.replace("REPLACE_ME", html_file.read())
            print("Temporarily wrote " + html_filename + " to " + template_filename)
            with open(gen_filename, "w+") as gen_file:
                gen_file.write(replacement_string)
                print("Wrote to " + gen_filename)                
                
                
                    
                    
                    
                    
                    
                    
                    
                
    

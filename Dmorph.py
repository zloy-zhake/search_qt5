import sys, os
os.system("cat Dsource_file.txt |apertium -d. kaz-morph >Dmorph_file.xml")
os.system("cat Dsource_file.txt |apertium -d. kaz-morph >Dmorph_file.txt")

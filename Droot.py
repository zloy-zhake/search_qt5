import sys, os
os.system("cat Dsource_file.txt|apertium -d. kaz-morph|sed -e 's/\$\W*\^/$\\n^/g'| cut -f2 -d'/'|cut -f1 -d '<'>Dsource_file_root.txt")  		

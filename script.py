#!/usr/bin/env python

import os
import sys
import shutil
import ftplib

input = "{query}"

"""
if len(sys.argv) < 3:
	name = sys.argv[1]
	url = "http://nicholasward.codes/" + name
else:
	name = sys.argv[1]
	url = sys.argv[2]
"""

name = input[:input.find(" ")]
url = input[input.find(" ")+1:]

if not url.startswith("http://") and not url.startswith("https://"):
	url = "http://" + url

shutil.rmtree("temp", ignore_errors = True)
os.mkdir("temp")

os.mkdir("temp/%s" % (name))

redirectfile = open("temp/%s/index.html" % (name), "a")

redirectfile.write("<!DOCTYPE html>\n")
redirectfile.write("<html>\n")
redirectfile.write("    <head>\n")
redirectfile.write("        <meta http-equiv='refresh' content='0; %s' />\n" % (url))
redirectfile.write("    </head>\n")
redirectfile.write("\n")
redirectfile.write("    <body>\n")
redirectfile.write("    </body>\n")
redirectfile.write("</html>\n")

redirectfile.close()

connection = ftplib.FTP("acit.us.com")
connection.login("nward", "") # (password goes here)


# Python 3.3 version
#files = list(connection.mlsd())
#filenames = [thing[0] for thing in files]

filenames = connection.nlst()

# Debug
#outputfile = open("/Users/npward/Desktop/output.txt", "a")
#outputfile.write("\n".join(filenames))
#outputfile.close()

created = False
if not name in filenames:
	redirectfile = open("temp/%s/index.html" % (name), "r")

	connection.mkd(name)
	connection.storlines("STOR %s/index.html" % (name), redirectfile)

	redirectfile.close()

	created = True
else:
	print("Redirect for \"%s\" already exists!" % name)

connection.close()

shutil.rmtree("temp", ignore_errors = True)

if created:
	print("Successfully created \"%s\" redirect!" % (name))

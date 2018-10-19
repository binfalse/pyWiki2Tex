#!/usr/bin/env python3
#
# Copyright (C) 2018 Martin Scharm <https://binfalse.de/contact/>
#
# This file is part of wiki2tex
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import wptools
import pypandoc
import argparse
import os
import errno
import requests


parser = argparse.ArgumentParser (
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description='wiki2tex - convert a wikipedia page to latex source code',
	epilog='''\
	
	
EXAMPLE:

If you, for example, want to retrieve the German Wikipedia page for
"Digitalisierung" and store it together with all images in
/tmp/latexproject, you would call the following:

python3 wiki2tex.py Digitalisierung --language de --dest /tmp/latexproject --imagedir /tmp/latexproject --overwrite''')
parser.add_argument ('page',
										 help='The page\'s name on Wikipedia')
parser.add_argument ('--language',
										 default='en',
										 help='The wikipedia language, defaults to en.')
parser.add_argument ('--dest',
										 default='./',
										 help='Where to store the tex document? If {DEST} does not end in `.tex`, we treat it as a directory. If {DEST} is a directory, we will create `{DEST}/{page}.tex`. {DEST} defaults to `./`. We will not overwrite files, unless called with --overwrite.')
parser.add_argument ('--imagedir',
										 help='Path to a directory to store the images of the article. If {IMAGEDIR} is empty, images are not retrieved. Will not overwrite images, unless called with --overwrite.')

parser.add_argument ('--overwrite',
										 action='store_true',
										 default=False,
										 help='Should existing files be overwritten?')


args = parser.parse_args()



# where to store the tex file?
targettex = args.dest
if os.path.isdir (targettex) or not targettex.endswith(".tex"):
	targettex = os.path.join (targettex, args.page + ".tex")

if os.path.exists (targettex) and not args.overwrite:
	raise IOError ("target file " + targettex + " exists -- will not overwrite it")


# make sure the parent directory exists
try:
	os.makedirs (os.path.abspath (os.path.join (targettex, os.pardir)))
except OSError as e:
	if e.errno != errno.EEXIST:
		raise



# retrieve page and write to disk
page = wptools.page (args.page, lang=args.language).get_parse ().get_more ()
with open (targettex, 'w') as o:
	o.write (pypandoc.convert (page.data['wikitext'], "latex", format="mediawiki"))


# download files if --imagedir was provided
if "files" in page.data and args.imagedir is not None:
	# make sure imagedir is a directory if given
	try:
		os.makedirs (args.imagedir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
	
	for image in page.data['files']:
		print ("downloading " + image)
		colon = image.find (":")
		if colon < 2:
			raise RuntimeError ("cannot find a colon in " + image)
		
		ifile = image[(colon + 1):].replace(" ", "_")
		iloc = os.path.join (args.imagedir, ifile)
		if os.path.exists (iloc) and not args.overwrite:
			print (iloc + " exists, will not overwrite it")
		
		r = requests.get('https://'+args.language+'.wikipedia.org/w/api.php?action=query&prop=imageinfo&format=json&iiprop=url&titles=File:' + ifile)
		if r.status_code != 200:
			print ("cannot find image location of " + image)
			continue
		
		j = r.json ()
		for k, p in j['query']['pages'].items():
			for ii in p['imageinfo']:
				with open(iloc, 'wb') as fd:
					r = requests.get(ii['url'], stream=True)
					for chunk in r.iter_content(chunk_size=128):
						fd.write(chunk)
				print ("stored image in " + iloc)
				break
			break


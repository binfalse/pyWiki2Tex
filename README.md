# pyWiki2Tex

Python tool to retrieve a page from Wikipedia and store it as a latex code file on disk. `pyWiki2Tex` can also retrieve all occurring images.

## Usage

    wiki2tex.py [-h]
                [--language LANGUAGE]
                [--dest DEST]
                [--imagedir IMAGEDIR]
                [--overwrite]
                page

with the following arguments:

* `page` the page name to retrieve
* `--language LANGUAGE`  The wikipedia language, defaults to en.
* `--dest DEST`          Where to store the tex document? If {DEST} does not end
in `.tex`, we treat it as a directory. If {DEST} is a
directory, we will create `{DEST}/{page}.tex`. {DEST}
defaults to `./`. We will not overwrite files, unless
called with --overwrite.
* `--imagedir IMAGEDIR`  Path to a directory to store the images of the article.
If {IMAGEDIR} is empty, images are not retrieved. Will
not overwrite images, unless called with --overwrite.
* `--overwrite`          Should existing files be overwritten?
* `-h`, `--help`           Show a help message and exit


## Example

Retrieve the German Wikipedia page for *Digitalisierung* and store it together with all images in `/tmp/latexproject`:

    python3 wiki2tex.py Digitalisierung --language de --dest /tmp/latexproject --imagedir /tmp/latexproject --overwrite


## Licence

    Copyright (C) 2018 Martin Scharm <https://binfalse.de/contact/>
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

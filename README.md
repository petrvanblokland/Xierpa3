
    Xierpa server
    Copyright(c) 2014+ buro@petr.com, www.petr.com, www.xierpa.com
   
    X I E R P A  3
    Distribution by the MIT License.

-----------------------------------------------------------------------------

    Version 0.8 beta

-----------------------------------------------------------------------------

## About

Xierpa3 is a framework for object base publications, using Components, Builders, 
Adapters and Attributes. Generating HTML5+CSS3 configurations (with or without PHP), 
or PDF, or pixel images. Live or as template files.

For now Xierpa3 is a proof-of-concept "gone live". This means that currently
installation may not be as automated and smooth as it will be and themes, examples
and documentation are not finished. Parts of Xierpa3 are still under development
right now. Classes are available in the source that are still being worked on and
tested. This will remain until version 1.0.

But Xierpa is already a great framework to start thinking about the creation of 
publications through objects, rather than writing websites in CSS+HTML (or PHP) directly. 

-----------------------------------------------------------------------------

### Getting started

The includes example site "doingbydesign" will include guided instructions how to get 
started with Python (www.python.org) in general and Xierpa3 in particular. 
The example sites are set up as an incremental sequence, starting with the most simple
"Hello world" site, and then adding styling, adapters, responsive behavior, multiple pages,
adapters such as PHP, etc. The final example is the complete documentation website for Xierpa3,
showing all the aspects of the system in code as well as page content.

The online version of the documentation site is available as soon as the functions in Xierpa3 are up to date.

Also under development is the Xierpa3App, an OSX desktop application that functions as a wrapper
around the Xierpa3 library. Since the application acts like a desktop webserver, it allows 
testing of the example sites without installing any Python libraries. Also it is the platform 
in which alterations can be made to existing style sets, buth by UI functions or by scripting.

The Xierpa3App will be available for download in the near future.
	
-----------------------------------------------------------------------------

### Architecture

The main types of classes are:
 * Components form the hierarchical set of building block of a site or a page.
 	Components can contain other components, forming a tree. Each components has a 
 	range of attributes that can be defined. In principle a component is not made
 	for a particular output or usage. 
 * Builders know how to convert a tree of components in a specific output format.
 	There a builders for CSS, SCSS, HTML (and later also for PDF and pixel images).
 * Adapters can be queried for content, by calling them with a standardized set of
 	methods and an item id when searching for a specific record. There are adapters
 	for Blurb text, for database access, XML file parsing, etc.
 * Attributes define values that are often used and need some kind of behavior,
 	depending on the type of the value and type of the output channel, such as
 	Shadow() and Gradient().
 	
-----------------------------------------------------------------------------

### Databases

A variety of database connections is possible: local and online SQL databases,
Amazon database services and S3. The amount of adapters has to be extended for
this Open Source versions of Xierpa3 to make it work. Currently PostgreSQL is 
supported, we aim to support MySQL as well in the near future.

-----------------------------------------------------------------------------

### History

Xierpa3 (2014) is based on XPyth (2002), Xierpa (2006) and Xierpa2 (2010).

XPyth, Xierpa and Xierpa2 were developed by Petr van Blokland and Torben Wilhelmsen.

-----------------------------------------------------------------------------

### Who

Xierpa3 is a product developed by:

Buro Petr van Blokland + Claudia Mens  
Rietveld 56  
2611 LM Delft  
The Netherlands  

Phone: +31 15 887 1233  
Mobile: +31 6 2421 9502  
Email: buro@petr.com  
FB & Twitter: @petrvanblokland  

#### Developers & Designers Contributing to Xierpa

 * [Petr van Blokland](mailto:buro@petr.com)
 * [Kirsten Langmuur](mailto:kirsten@petr.com)
 * [Michiel Kauw-A-Tjoe](mailto:michiel@petr.com)
 * [Torben Wilhelmsen](mailto:torben@wil.dk)

#### Contributers of code
 * Filibuster by Erik van Blokland and Jonathan Hoefler.

#### Published by he MIT License
 * http://opensource.org/licenses/MIT

 -----------------------------------------------------------------------------

### Rights

Copyright (c) 2014+ Buro Petr van Blokland + Claudia Mens

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

 -----------------------------------------------------------------------------

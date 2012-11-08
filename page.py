#!/usr/bin/python
###########################################################################
# Purpose: Notice object.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

class Page:
	def __init__( self ):
		self.page  = ''
	def getPage( self ):
		self.page += 'showpage\n'
		return self.page
		
		
		
		

# /Times-Roman findfont   % Get the basic font
# 20 scalefont            % Scale the font to 20 points
# setfont                 % Make it the current font

# newpath                 % Start a new path
# 72 72 moveto            % Lower left corner of text at (72, 72)
# (Hello, world!) show    % Typeset "Hello, world!"

# showpage

# %!PS-Adobe-2.0

# %%Pages: 2
# %%Page: 1 1
# newpath
# 100 100 moveto
# 400 400 lineto
# closepath 
# 5 setlinewidth
# stroke
# showpage
# %%Page: 2 2
# newpath
# 100 400 moveto
# 400 100 lineto
# closepath
# 10 setlinewidth
# stroke
# showpage

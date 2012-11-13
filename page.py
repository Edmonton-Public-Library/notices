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
        self.page = ''
    def setHeadMessages( text ):
        pass
    def setItems( text ):
        pass
    def setFootMessages( text ):
        pass
    def setAddress( text ):
        pass
    def __str__( self ):
        return self.page
        
class PostscriptPage( Page ):
    def __init__( self, pageNumber, debug=False ):
		if debug == True:
			self.page  = '%!PS-Adobe-2.0\n\n/inch {\n\t72 mul\n} def\n'
			self.page += '/perfline {\n'
			self.page += '[6 3] 3 setdash\n'
			self.page += 'stroke\n'
			self.page += 'newpath\n'
			self.page += '} def\n'
			self.page += '/fineperfline {\n'
			self.page += 'gsave\n'
			self.page += '0.5 setgray\n'
			self.page += '[4 2] 0 setdash\n'
			self.page += 'stroke\n'
			self.page += 'grestore\n'
			self.page += 'newpath\n'
			self.page += '} def\n'
			self.page += '/pageborder{\n'
			self.page += '0.5 inch 0  inch moveto\n'
			self.page += '0.5 inch 11 inch lineto\n'
			self.page += '8   inch 0  inch moveto\n'
			self.page += '8   inch 11 inch lineto\n'
			self.page += '0.5 setlinewidth\n'
			self.page += 'perfline\n'
			self.page += '0   inch 3.15625 inch moveto\n'
			self.page += '8.5 inch 3.15625 inch lineto\n'
			self.page += '0.25 setlinewidth\n'
			self.page += 'fineperfline\n'
			self.page += '0   inch 3.625 inch moveto\n'
			self.page += '8.5 inch 3.625 inch lineto\n'
			self.page += 'fineperfline\n'
			self.page += '0   inch 4.15625 inch moveto\n'
			self.page += '8.5 inch 4.15625 inch lineto\n'
			self.page += 'fineperfline\n'
			self.page += '0   inch 6.90625 inch moveto\n'
			self.page += '8.5 inch 6.90625 inch lineto\n'
			self.page += 'fineperfline\n'
			self.page += '0   inch 7.3125  inch moveto\n'
			self.page += '8.5 inch 7.3125  inch lineto\n'
			self.page += 'fineperfline\n'
			self.page += '0   inch 10.5    inch moveto\n'
			self.page += '8.5 inch 10.5    inch lineto\n'
			self.page += 'fineperfline\n'
			self.page += '} def\n'
			self.page += '/Times-Roman findfont\n11 scalefont\nsetfont\n'
			self.page += '%%Pages: 1\n'
		self.page += '%%Page: 1 1\n'
		if debug == True:
			self.page += 'pageborder\n'
		self.page += self.__next_line__( 4, 100, ['Name Here', 'Address line one', 'Address line two'], 12 )
		# self.page += '/ppi 100 def\n'
		# self.page += 'newpath\n'
		# self.page += '4 inch ppi moveto\n'
		# self.page += '(Balzac Billy) show\n'
		# self.page += 'newpath\n'
		# self.page += '/ppi ppi 20 sub def\n'
		# self.page += '4 inch ppi moveto\n'
		# self.page += '(12345 123 Street) show\n'
		
    def __next_line__( self, x, y, lines, ptKerning=20 ):
		# comment
		block = '/ppi ' + str(y) + ' def\n'
		for line in lines:
			block += 'newpath\n'
			block += str(x) + ' inch ppi moveto\n'
			block += '(' + line + ') show\n'
			block += '/ppi ppi ' + str(ptKerning) + ' sub def\n'
		return block
		
		
    def setHeadMessages( text ):
        pass
    def setItems( text ):
        pass
    def setFootMessages( text ):
        pass
    def setAddress( text ):
        pass
    def __str__( self ):
		self.page += 'showpage\n'
		return self.page  
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	page = PostscriptPage( 1, True )
	f = open( 'test.ps', 'w' )
	f.write( str(page) )
	f.close()

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

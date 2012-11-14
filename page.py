#!/usr/bin/python
###########################################################################
# Purpose: Notice object.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

POINTS = 72.0
class Page:
    def __init__( self ):
        self.page = ''
    def setTitle( self ):
        pass
    def setHeadMessages( self, text ):
        pass
    def setItems( self, text ):
        pass
    def setFootMessages( self, text ):
        pass
    def setAddress( self, text ):
        pass
    def __str__( self ):
        return self.page
        
class PostscriptPage( Page ):
    def __init__( self, pageNumber, debug=False, font='Times-Roman', fontsize=12.0, kerning=14.0 ):
        self.page     = ''
        self.font     = font
        self.fontSize = fontsize
        self.kerning  = kerning
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
            self.page += '/' + self.font + ' findfont\n' + str( self.fontSize ) + ' scalefont\nsetfont\n'
            self.page += '%%Pages: 1\n'
        self.page += '%%Page: 1 1\n'
        if debug == True:
            self.page += 'pageborder\n'
		
    def __set_text_block__( self, lines, x, y, lowerBound ):
		# check if you can place all this text before placemnet
        x_s = self.__to_points__( x )
        y_s = self.__to_points__( y )
        if ( y * POINTS - ( len( lines ) * self.kerning )) < ( lowerBound * POINTS ):
            return False
        for line in lines:
            self.page += 'newpath\n'
            self.page += x_s + ' ' + y_s + ' moveto\n'
            self.page += '(' + line + ') show\n'
            y -= (self.kerning / POINTS)
            y_s = self.__to_points__( y )
        return True
		
    def setTitle( self, text, x, y, centre=True ):
        if centre == True:
            midPage = 4.25 * POINTS
            x = midPage - ( len( text ) * 8 ) / 2
        x_s = self.__to_points__( x )
        y_s = self.__to_points__( y )
        self.page += 'newpath\n'
        self.page += x_s + ' ' + y_s + ' moveto\n'
        self.page += '(' + text + ') show\n'
    def setHeadMessages( self, text ):
        pass
    def setItems( self, text ):
        pass
    def setFootMessages( self, text ):
        pass
    def setAddress( self, text, x, y, m=0.25 ):
        return self.__set_text_block__( text, x, y, m )
    def __str__( self ):
		self.page += 'showpage\n'
		return self.page
    def __to_points__( self, n ):
        return str( n * POINTS )
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    page = PostscriptPage( 1, True )
    print page.setAddress( ['Name Here', 'Address line one', 'Address line two', 'Address line Three', 'P0S 7A1'], 4, 1.75 )
    f = open( 'test.ps', 'w' )
    f.write( str(page) )
    f.close()

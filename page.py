#!/usr/bin/python
###########################################################################
# Purpose: Notice object.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          0.0 - Dev.
###########################################################################

# Takes a long string and returns an array of strings broken to fit within 
# a page boundary.
# param: text - string
# param: preserve white space - True keeps leading white space false strips it.
# return: an array of strings.
def breakLongLines( text, preserveWhiteSpace=False ):
    page = PostscriptPage( 0 )
    return page.__break_line__( [text], preserveWhiteSpace )
    
POINTS = 72.0
class Page:
    def __init__( self ):
        self.page = ''
    def setTitle( self ):
        pass
    def setTextBlock( self, text ):
        pass
    def setLine( self, text ):
        pass
    def __str__( self ):
        return self.page

        
class PostscriptPage( Page ):
    def __init__( self, pageNumber, debug=False, font='Courier', fontsize=10, kerning=11.0 ):
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
	
    # Sets a list of strings at the appropriate location
    # param:  lines - array of strings to be laid out on the page
    # param:  x - x coordinate of the first line of the array of strings. The first
    #         placement is based on the bottom left corner of the first character of the first
    #         line. In Postscript bottom refers to the lowest point on a non-decending character.
    # param:  y - y coordinate with origin (0,0) at the lower left corner of the page.
    # param:  dry run - True if you want the text to appear, false if you want the location of 
    #         where the bottom of the text box would have been if the text was to be laid out.
    # return: float - the y location of the last line printed.
    def __set_text_block__( self, lines, x, y, dryRun=False ):
        for line in lines:
            if dryRun == False:
                self.__set_text__( line, x, y )
            y -= ( self.kerning / POINTS )
        return y
    
    # Writes a line of text to the location given.
    # param:  line - string to be laid out on the page
    # param:  x - x coordinate of the string.
    # param:  y - y coordinate with origin (0,0) at the lower left corner of the page. 
    def __set_text__( self, line, x, y ):
        x_s = self.__to_points__( x )
        y_s = self.__to_points__( y )
        self.page += 'newpath\n' + x_s + ' ' + y_s + ' moveto\n(' + line + ') show\n'
    # Default method that stringifies object.
    # param:  
    # return: the postscript string of this object.
    def __str__( self ):
		self.page += 'showpage\n'
		return self.page
        
    # Converts the argument into points
    # param:  n float - the value to convert.
    # return: n * 72 as a string
    def __to_points__( self, n ):
        return str( n * POINTS )
    
    # Breaks long lines from a block of text into chunks that will fit within
    # the notice boundaries (line length < 6.5").
    # param:  block - array of strings.
    # param:  preserveWhiteSpace - True to keep leading white space before words and False otherwise.
    # return: New array of strings chopped nearest word boundary fitted to page boundary.
    def __break_line__( self, block, preserveWhiteSpace ):
        maxCharsPerLine = ( 6.5 * POINTS ) / ( self.fontSize * 0.55 )
        textBlock = []
        thisLine = ''
        for line in block:
            if len( line ) <= maxCharsPerLine:
                textBlock.append( line )
                continue
            words = []
            # If items don't preserve whitespace they end up looking odd.
            if preserveWhiteSpace == True:
                words = self.__split__( line )
            else: # this is for messages that are just one long line.
                words = line.split()
            for word in words:
                if len( thisLine ) + len( word ) <= maxCharsPerLine:
                    thisLine += word + ' '
                else:
                    textBlock.append( thisLine[:-1] )
                    thisLine  = word + ' '
            textBlock.append( thisLine[:-1] )
        return textBlock
	
    # Splits a line into words but keeps the leading spacing.
    # param:  sentence - string of words
    # return: array of words with leading spaces intact.
    def __split__( self, sentence ):
        words = sentence.split()
        start   = 0
        end     = 0
        spcWords = []
        for word in words:
            end = sentence.find( word, start ) + len(word)
            spcWords.append( sentence[start:end] )
            start = end
        return spcWords
    
    # Sets the title on the page in bold.
    # param:  text - Title string
    # param:  x - coordinate in inches.
    # param:  y - coordinate in inches.
    # param:  size - float of size of text for the title in points.
    # param:  centre - True if the text is to be centered and false otherwise.
    # return: 
    def setTitle( self, text, x, y, size=18.0, centre=True ):
        if centre == True:
            midPage = 4.25 * POINTS
            # this is a loosy-goosy method of centring the string.
            x = midPage - ( len( text ) * ( size * 0.75 ) ) / 2.0
            x_s = str( x )
        else:
            x_s = self.__to_points__( x )
        y_s = self.__to_points__( y )
        self.page += 'gsave\n'
        self.page += '/' + self.font + '-Bold findfont\n' + str( size ) + ' scalefont\nsetfont\n'
        self.page += 'newpath\n'
        self.page += x_s + ' ' + y_s + ' moveto\n'
        self.page += '(' + text + ') show\n'
        self.page += 'grestore\n'
    
    # Sets a block of text returning the y location of the last line in inches.
    # param:  list of strings of a block
    # param:  x - x coord.
    # param:  y - y coord in inches.
    # param:  preserverWhiteSpace True to save leading white space on line breaking False will remove it.
    # return: last y coord in inches.
    def setTextBlock( self, block, x, y, preserverWhiteSpace, bold=False ):
        textBlock =  self.__break_line__( block, preserverWhiteSpace )
        if bold == True:
            self.page += 'gsave\n'
            self.page += '/' + self.font + '-Bold findfont\n' + str( self.fontSize ) + ' scalefont\nsetfont\n'
        lastY = self.__set_text_block__( textBlock, x, y )
        if bold == True:
            self.page += 'grestore\n'
        return lastY
        
    # Sets a single line of text.
    # param:  String to place.
    # param:  x - x coord.
    # param:  y - y coord in inches.
    # return: 
    def setLine( self, text, x, y, bold=False ):
        if bold == True:
            self.page += 'gsave\n'
            self.page += '/' + self.font + '-Bold findfont\n' + str( self.fontSize ) + ' scalefont\nsetfont\n'
        self.__set_text__( text, x, y )
        if bold == True:
            self.page += 'grestore\n'
    
    # Writes a predefined instruction to the postscript file.
    def setInstruction( self, instruction ):
        self.page += instruction + '\n'
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    page = PostscriptPage( 1, True )
    page.setTextBlock( ['Name Here', 'Address line one', 'Address line two', 'Address line Three', 'P0S 7A1'], 4, 1.75, False )
    msg = ['Statement produced: Friday, August 24 2012']
    nextLine = page.setTextBlock( msg, 0.875, 9.875, False )
    msg = ['Our records indicate that the following amount(s) is outstanding by more than 15 days.  This may block your ability to borrow or to place holds or to renew materials online or via our telephone renewal line. Please go to My Account at http://www.epl.ca/myaccount for full account details.']
    nextLine = page.setTextBlock( msg, 0.875, (nextLine - 0.18), False )
    msg = ['  1   The lion king 1 1/2 [videorecording] / [directed by Bradley Raymond].',
    '      Raymond, Bradley.',
    '      $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $1.60']
    nextLine = page.setTextBlock( msg, 0.875, (nextLine - 0.18), True, True )
    page.setTitle('Test Title', 4.25, 10.1875 )
    page.setLine('Statement 1 of 2', 0.875, 4.5 )
    f = open( 'test.ps', 'w' )
    f.write( str(page) )
    f.close()

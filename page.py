#!/usr/bin/env python
###########################################################################
#
#    Copyright (C) 2012 - 2023  Andrew Nisbet, Edmonton Public Library
# The Edmonton Public Library respectfully acknowledges that we sit on
# Treaty 6 territory, traditional lands of First Nations and Metis people.
# Collects all the notices required for the day and coordinates convertion to PDF.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#
# Purpose: Notice object.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          1.0 - Refactored classes to simplify interfaces and balance 
#                method responsibilities.
###########################################################################
import sys
from reportlab.pdfgen.canvas import Canvas

INCH = 72.0
class Page:
    def __init__(self, pageNumber:int, configs:dict, debug:bool):
        self.page            = ''
        self.configDict      = configs
        self.font            = self.configDict.get('font')
        self.fontSize        = self.configDict.get('fontSize')
        self.kerning         = self.configDict.get('kerning')  # points.
        self.leftMargin      = self.configDict.get('leftMargin')    # inches
        self.fontSizeTitle   = 18.0    # points
        self.xTitle          = 3.3125  # inches was 4.25, 10.1875
        self.yTitle          = 10.1875 # inches
        self.yHeader         = 9.5625  # inches
        self.xHeader         = self.leftMargin # inches
        self.xDate           = self.leftMargin # inches
        self.yDate           = 9.875   # inches
        self.xFooter         = self.leftMargin # inches
        self.yFooter         = 4.5     # inches
        self.xAddressBlock   = 3.25    # inches
        self.yAddressBlock   = 1.75    # inches
        self.itemYMin        = 5.0     # inches
        # The first page is set to the bottom of the header, the second page will print just below the statement
        self.nextLine        = self.yDate
        self.isIncomplete    = True # marker that page has been finalized or not.

    # Writes a line of text to the location given. Origin (0,0) is at the
    # bottom left of the page for both PS and PDF.
    # param:  line - string to be laid out on the page
    # param:  x - x coordinate of the string.
    # param:  y - y coordinate.
    # param: bold:bool - True if bold text to be used and false otherwise. 
    # param: fontSize:float - Optional if provided will set font size.  
    # return: y coordinate of the next line of text. 
    def __set_text__(self, line:str, x:float, y:float, bold:bool=False, fontSize:float=None) ->float:
        pass

    # Sets a list of strings at the appropriate location
    # param:  lines - array of strings to be laid out on the page
    # param:  x - x coordinate of the first line of the array of strings. The first
    #         placement is based on the bottom left corner of the first character of the first
    #         line. In Postscript bottom refers to the lowest point on a non-decending character.
    # param:  y - y coordinate with origin (0,0) at the lower left corner of the page.
    # return: float - the y location of the last line printed.
    def __set_text_block__(self, lines:list, x:float, y:float, bold:bool=False) ->float:
        pass

    # Sets the title on the page in bold.
    # param:  text - Title string
    def setTitle( self, text:str ):
        self.__set_text__(text, self.xTitle, self.yTitle, bold=True, fontSize=self.fontSizeTitle)

    # Returns the height of the block of text in inches.
    # param:  list of lines of address text.
    # return: None, but sets the self.nextLine in the super class.
    def setAddress( self, textBlock:list ):
        # TODO: Do we need this var and how it is set??
        self.nextLine = self.__set_text_block__( textBlock, self.xAddressBlock, self.yAddressBlock )
        
    # Prints the argument text at the appropriate position
    # param:  text - single string.
    def setStatementDate( self, text:str ):
        return self.__set_text__(text, self.xDate, self.yDate)
    
    # Sets the 'page n of m' message.
    # param: text:str statement.
    # return: None 
    def setStatementCount( self, text:str ):
        self.__set_text__( text, self.xFooter, self.yFooter )

    # Sets an item text block.
    # param:  List of strings that make up an item description.
    # param:  x - x coordinate of the text block (in.).
    # param:  y - y coord in inches.
    # return: y position of the next line of text.
    def setItem(self, textBlock:list, x:float, y:float):
        return self.__set_text_block__(textBlock, x, y, bold=True)
        
    # Signals that the caller is finished with the page.
    # param:  None
    # return: None, sets the super class' isIncomplete flag to false.
    def finalize(self):
        self.isIncomplete = False
    
    # This page returns True if the argument item can be fit on this page and False
    # otherwise. Postscript's origin (0, 0) is in the lower left corner, so the closer
    # to zero y gets the closer to the bottom of the page. Items can't print below 
    # the itemYMin which is currently set to 5.0 inches from the bottom of the form.
    def isRoomForItem( self, textBlock:list, lastYPosition:float ):
        myBlock = self.__break_lines__( textBlock )
        y = lastYPosition - ( len( myBlock ) * ( self.kerning / INCH ))
        if y >= self.itemYMin:
            return True
        else:
            return False

    # Used for PostScript, but and is optional in the subclass.
    # param: instruction:str - Inserts an arbitrary instruction in the output file code. 
    def setInstruction(self, instruction:str):
        pass

    # Breaks long lines from a block of text into chunks that will fit within
    # the notice boundaries (line length < 6.5").
    # param:  block - array of strings.
    # return: New array of strings chopped nearest word boundary fitted to page boundary.
    def __break_lines__( self, block:list ):
        maxCharsPerLine = ( 6.5 * INCH ) / ( self.fontSize * 0.55 )
        textBlock = []
        prevLine = ''
        while ( True ):
            line1 = prevLine
            try:
                if len( line1 ) == 0: # This stops an intial ' ' character for the first string.
                    line2 = block.pop( 0 )
                    if len( line2 ) <= maxCharsPerLine: # don't wrap lines that are smaller than max size.
                        textBlock.append( line2 )
                        continue
                else:
                    line2 = line1 + ' ' + block.pop( 0 )
            except IndexError:
                newLines = self.__break_line__( line1, maxCharsPerLine )
                textBlock.extend( newLines )
                break
            newLines = self.__break_line__( line2, maxCharsPerLine )
            # extend the array to include all but the last line, it becomes the first line next time.
            textBlock.extend( newLines[:-1] ) 
            prevLine = newLines[-1]
        for line in textBlock:
            block.append( line )
        return textBlock
    
    # Breaks a single string into an block of text (array) of one element if the 
    # string didn't need to be split.
    # param:  text string of text
    # param:  preserveWhitespace  - if True all white space is presevered, and if False words are separated by a single whitespace.
    # return: list of split strings.
    def __break_line__( self, text:str, maxCharsPerLine:int ):
        thisLine = ''
        textBlock = []
        if len( text ) <= maxCharsPerLine:
            if len( text) > 0: # this stops excessive spacing between items.
                textBlock.append( text )
            return textBlock
        else: # we will split the long strings.
            words = self.__split__( text )
            for word in words:
                if len( thisLine ) + len( word ) <= maxCharsPerLine:
                    thisLine += word
                else: # if the word doesn't fit, append what's on the line now and then make a new one starting with the current word.
                    textBlock.append( thisLine )
                    thisLine = word.lstrip()
            textBlock.append( thisLine )
        return textBlock
    
    # Splits a line into words but keeps the leading spacing.
    # param:  sentence - string of words
    # return: array of words with leading spaces intact.
    def __split__( self, sentence:str ):
        words    = sentence.split()
        start    = 0
        end      = 0
        spcWords = []
        for word in words:
            end = sentence.find( word, start ) + len(word)
            spcWords.append( sentence[start:end] )
            start = end
        return spcWords

    # The string version of this object.
    def __str__( self ):
        return self.page

class PdfPage(Page):
    # Configuration dict currently must contain font, fontsize, and kerning.
    def __init__(self, pageNumber:int, configs:dict, debug:bool=False):
        super().__init__(pageNumber, configs, debug)
        self.canvas = configs.get('canvas')
        if not self.canvas:
            print(f"*error, PdfPage expected canvas object to be a member of the configs dictionary.")
            # Signal the shell there was a problem.
            sys.exit(-1)
        self.isIncomplete = True

    # Writes a line of text to the location given. Origin (0,0) is at the
    # bottom left of the page for both PS and PDF.
    # param:  line - string to be laid out on the page
    # param:  x - x coordinate of the string.
    # param:  y - y coordinate.
    # param: bold:bool - True if bold text to be used and false otherwise. 
    # param: fontSize:float - Optional if provided will set font size.  
    # return: y coordinate of the next line of text. 
    def __set_text__(self, line:str, x:float, y:float, bold:bool=False, fontSize:float=None) ->float:
        tmpFontSize = round(self.fontSize)
        tmpFont = self.font
        if fontSize or bold:
            self.canvas.saveState()
            if fontSize:
                tmpFontSize = round(fontSize)
            if bold:
                tmpFont = f"{self.font}-Bold"
        self.canvas.setFont(tmpFont, tmpFontSize)
        self.canvas.drawString(x * INCH, y * INCH, line)
        if fontSize or bold:
            self.canvas.restoreState()
        return y - (self.kerning / INCH)
    
    # Sets a list of strings at the appropriate location
    # param:  lines - array of strings to be laid out on the page
    # param:  x - x coordinate of the first line of the array of strings. The first
    #         placement is based on the bottom left corner of the first character of the first
    #         line. In Postscript bottom refers to the lowest point on a non-decending character.
    # param:  y - y coordinate with origin (0,0) at the lower left corner of the page.
    # return: float - the y location of the last line printed.
    def __set_text_block__(self, lines:list, x:float, y:float, bold:bool=False) ->float:
        textBlock = self.__break_lines__(lines)
        for line in textBlock:
            y = self.__set_text__(line, x, y, bold)
        return y
    
class PostscriptPage( Page ):
    # Configuration dict currently must contain font, fontsize, and kerning.
    def __init__( self, pageNumber:int, configs:dict, debug=False):
        super().__init__(pageNumber, configs, debug)
        if debug == True:
            self.page  = '%!PS-Adobe-2.0\n\n'
            self.page  = '/' + self.font + ' findfont\n' + str( self.fontSize ) + ' scalefont\nsetfont\n'
            self.page += '%%Pages: 1\n'
        self.page += '%%Page: ' + str( pageNumber ) + ' ' + str( pageNumber ) + '\n'
        self.isIncomplete = True # marker that page is complete.
    
    # Sets a page specific instruction.
    # param:  instruction - make sure it has been predefined in the head of the PS file.
    # return: 
    def setInstruction( self, instruction ):
        self.page += instruction + '\n'
        
    # Writes a line of text to the location given. Origin (0,0) is at the
    # bottom left of the page for both PS and PDF.
    # param:  line - string to be laid out on the page
    # param:  x - x coordinate of the string.
    # param:  y - y coordinate.
    # param: bold:bool - True if bold text to be used and false otherwise. 
    # param: fontSize:float - Optional if provided will set font size.  
    # return: y coordinate of the next line of text. 
    def __set_text__(self, line:str, x:float, y:float, bold:bool=False, fontSize:float=None) ->float:
        myFontSize = self.fontSize
        if fontSize or bold:
            self.page += f"gsave\n"
            if fontSize:
                myFontSize = fontSize
            if bold:
                self.page += f"/{self.font}-Bold findfont\n{str(myFontSize)} scalefont\nsetfont\n"
        x_s = str( x * INCH )
        y_s = str( y * INCH )
        # sanitize the line parens are special symbols in PS.
        line = line.replace( '(', '\(' )
        line = line.replace( ')', '\)' )
        self.page += f"newpath\n{x_s} {y_s} moveto\n({line}) show\n"
        if fontSize or bold:
            self.page += f"grestore\n"
        return y - ( self.kerning / INCH ) # convert points to inches to keep y in sync
    
    # Sets a list of strings at the appropriate location
    # param:  lines - array of strings to be laid out on the page
    # param:  x - x coordinate of the first line of the array of strings. The first
    #         placement is based on the bottom left corner of the first character of the first
    #         line. In Postscript bottom refers to the lowest point on a non-decending character.
    # param:  y - y coordinate with origin (0,0) at the lower left corner of the page.
    # return: float - the y location of the last line printed.
    def __set_text_block__(self, lines:list, x:float, y:float, bold:bool=False) ->float:
        if bold:
            self.page += 'gsave\n'
            self.page += '/' + self.font + '-Bold findfont\n' + str( self.fontSize ) + ' scalefont\nsetfont\n'
        for line in lines:
            y = self.__set_text__(line, x, y)
        if bold:
            self.page += 'grestore\n'
        return y

    # Default method that stringifies object.
    # param:  
    # return: the postscript string of this object.
    def __str__( self ):
        self.page += f"showpage"
        return self.page

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # Then do the Postscript page tests. 
    doctest.testfile("page.tst")
    print(f"Done, check files")

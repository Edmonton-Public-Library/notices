#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
#  1.1 Added contextual adding other TTFonts for better Unicode display
#      over Helvetica, Courier, and Times.
###########################################################################
import sys
import re
from reportlab.pdfgen.canvas import Canvas

INCH = 72.0
class Page:
    def __init__(self, pageNumber:int, configs:dict, debug:bool):
        self.debug           = debug
        self.page            = []
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
        self.isIncomplete    = True # marker that page has been finalized or not.
        self.pageNumber      = pageNumber

    # Writes a line of text to the location given. Origin (0,0) is at the
    # bottom left of the page for both PS and PDF.
    # param:  line - string to be laid out on the page
    # param:  x - x coordinate of the string.
    # param:  y - y coordinate.
    # param: bold:bool - True if bold text to be used and false otherwise. 
    # param: fontSize:float - Optional if provided will set font size.  
    # return: y coordinate of the next line of text. 
    def __set_text__(self, line:str, x:float, y:float, bold:bool=False, fontSize:float=None):
        # Format section separators like '=========...' to not overrun the side of the page. 
        if re.search("={5,}", line):
            line = '     ' + '=' * 41
        return line

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
    def setTitle(self, text:str):
        self.__set_text__(text, self.xTitle, self.yTitle, bold=True, fontSize=self.fontSizeTitle)

    # Returns the height of the block of text in inches.
    # param:  list of lines of address text.
    # return: None.
    def setAddress(self, textBlock:list):
        self.__set_text_block__(textBlock, self.xAddressBlock, self.yAddressBlock)
        
    # Prints the argument text at the appropriate position
    # param:  text - single string.
    # return: None
    def setStatementDate(self, text:str):
        self.__set_text__(text, self.xDate, self.yDate)
    
    # Sets the 'page n of m' message.
    # param: text:str statement.
    # return: None 
    def setStatementCount(self, text:str):
        self.__set_text__(text, self.xFooter, self.yFooter)

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
    def isRoomForItem(self, textBlock:list, lastYPosition:float):
        myBlock = self.__break_lines__(textBlock)
        y = lastYPosition - (len(myBlock) * (self.kerning / INCH))
        if y >= self.itemYMin:
            return True
        else:
            return False

    # Breaks long lines from a block of text into chunks that will fit within
    # the notice boundaries (line length < 6.5").
    # param:  block - array of strings.
    # return: New array of strings chopped nearest word boundary fitted to page boundary.
    def __break_lines__(self, block:list):
        maxCharsPerLine = (6.5 * INCH) / (self.fontSize * 0.55)
        textBlock = []
        prevLine = ''
        while (True):
            line1 = prevLine
            try:
                if len(line1) == 0: # This stops an intial ' ' character for the first string.
                    line2 = block.pop(0)
                    if len(line2) <= maxCharsPerLine: # don't wrap lines that are smaller than max size.
                        textBlock.append(line2)
                        continue
                else:
                    line2 = line1 + ' ' + block.pop(0)
            except IndexError:
                newLines = self.__break_line__(line1, maxCharsPerLine)
                textBlock.extend(newLines)
                break
            newLines = self.__break_line__(line2, maxCharsPerLine)
            # extend the array to include all but the last line, it becomes the first line next time.
            textBlock.extend(newLines[:-1]) 
            prevLine = newLines[-1]
        for line in textBlock:
            block.append(line)
        return textBlock
    
    # Breaks a single string into an block of text (array) of one element if the 
    # string didn't need to be split.
    # param:  text string of text
    # param:  preserveWhitespace  - if True all white space is presevered, and if False words are separated by a single whitespace.
    # return: list of split strings.
    def __break_line__(self, text:str, maxCharsPerLine:int):
        thisLine = ''
        textBlock = []
        if len(text) <= maxCharsPerLine:
            if len(text) > 0: # this stops excessive spacing between items.
                textBlock.append(text)
            return textBlock
        else: # we will split the long strings.
            words = self.__split__(text)
            for word in words:
                if len(thisLine) + len(word) <= maxCharsPerLine:
                    thisLine += word
                else: # if the word doesn't fit, append what's on the line now and then make a new one starting with the current word.
                    textBlock.append(thisLine)
                    thisLine = word.lstrip()
            textBlock.append(thisLine)
        return textBlock
    
    # Splits a line into words but keeps the leading spacing.
    # param:  sentence - string of words
    # return: array of words with leading spaces intact.
    def __split__(self, sentence:str):
        words    = sentence.split()
        start    = 0
        end      = 0
        spcWords = []
        for word in words:
            end = sentence.find(word, start) + len(word)
            spcWords.append(sentence[start:end])
            start = end
        return spcWords

    # The string version of this object.
    def __str__(self):
        return '\n'.join(self.page)

    # Adds folds, perferations, and registration marks for debugging. 
    def addRegistrationMarks(self):
        pass

# This class stores all the instructions on a list and then executes 
# the PDF generation code as lambda instructions.
class PdfPage(Page):
    # Configuration dict currently must contain font, fontsize, and kerning.
    def __init__(self, pageNumber:int, configs:dict, debug:bool=False):
        super().__init__(pageNumber, configs, debug)
        self.canvas = configs.get('canvas')
        # Replace 'DejaVuSans.ttf' with the path to a Unicode font file on your system
        # Helvetica just cannot display the extended characters of Vietnamese so switch
        # to DejaVuSans or other if required.
        # pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        ### Warning this overrides any font selection set by the parameters which is 
        if self.font != 'Courier' and self.font != 'Helvetica' and self.font != 'Times':
            # Required for Unicode True Type Fonts.
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            pdfmetrics.registerFont(TTFont(self.font, f"{self.font}.ttf"))
        if not self.canvas:
            print(f"*error, PdfPage expected canvas object to be a member of the configs dictionary.")
            # Signal the shell there was a problem.
            sys.exit(-1)
        self.isIncomplete = True
        if self.debug:
            self.addRegistrationMarks()
        # Finish the previous sheet or Pdf will wrap over the top of the page again if this is not set.
        if self.pageNumber > 1:
            self.page.append(lambda: self.canvas.showPage())

    # Writes a line of text to the location given. Origin (0,0) is at the
    # bottom left of the page for both PS and PDF.
    # param:  line - string to be laid out on the page
    # param:  x - x coordinate of the string.
    # param:  y - y coordinate.
    # param: bold:bool - True if bold text to be used and false otherwise. 
    # param: fontSize:float - Optional if provided will set font size.  
    # return: y coordinate of the next line of text. 
    def __set_text__(self, line:str, x:float, y:float, bold:bool=False, fontSize:float=None) ->float:
        line = super().__set_text__(line, x, y, bold, fontSize)
        tmpFontSize = round(self.fontSize)
        tmpFont = self.font
        if fontSize or bold:
            self.page.append(lambda: self.canvas.saveState())
            if fontSize:
                tmpFontSize = round(fontSize)
            if bold:
                tmpFont = f"{self.font}-Bold"
                try:
                    self.canvas.setFont(tmpFont, tmpFontSize)
                except KeyError:
                    # Go without bold.
                    tmpFont = f"{self.font}"
        self.page.append(lambda: self.canvas.setFont(tmpFont, tmpFontSize))
        self.page.append(lambda: self.canvas.drawString(x * INCH, y * INCH, line))
        if fontSize or bold:
            self.page.append(lambda: self.canvas.restoreState())
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

    # Signals that the caller is finished with the sheet.
    # param:  None
    # return: None, sets the super class' isIncomplete flag to false.
    def finalize(self):
        if self.debug:
            self.addRegistrationMarks()
        self.isIncomplete = False

    # Returns the height of the block of text in inches.
    # param:  list of lines of address text.
    # return: None.
    def setAddress(self, textBlock:list):
        self.__set_text_block__(textBlock, self.xAddressBlock, self.yAddressBlock)
        
    
    # Adds folds, perferations, and registration marks for debugging. 
    def addRegistrationMarks(self):
        self.page.append(lambda: self.canvas.saveState())
        self.page.append(lambda: self.canvas.setStrokeColorRGB(0, 0, 0))
        self.page.append(lambda: self.canvas.setLineWidth(0.5))
        self.page.append(lambda: self.canvas.setDash([6,3], 3))
        # Left and right page boundaries
        self.page.append(lambda: self.canvas.line(0.5 * INCH, 0.0 * INCH, 0.5 * INCH, 11.0 * INCH))
        self.page.append(lambda: self.canvas.line(8.0 * INCH, 0.0 * INCH, 8.0 * INCH, 11.0 * INCH))
        # Lowest perferation line
        self.page.append(lambda: self.canvas.line(0.0 * INCH, 3.09375 * INCH, 8.5 * INCH, 3.09375 * INCH))
        # Fold line lower 1/3
        self.page.append(lambda: self.canvas.line(0.0 * INCH, 3.5625 * INCH, 8.5 * INCH, 3.5625 * INCH))
        # Fine perforation above fold lower fold line.
        self.page.append(lambda: self.canvas.line(0.0 * INCH, 4.09375 * INCH, 8.5 * INCH, 4.09375 * INCH))
        # Fine perferation below top fold line.
        self.page.append(lambda: self.canvas.line(0.0 * INCH, 6.84375 * INCH, 8.5 * INCH, 6.84375 * INCH))
        # Top fold line
        self.page.append(lambda: self.canvas.line(0.0 * INCH, 7.275 * INCH, 8.5 * INCH, 7.275 * INCH))
        # Top-most tear line perferation.
        self.page.append(lambda: self.canvas.line(0.0 * INCH, 10.4375 * INCH, 8.5 * INCH, 10.4375 * INCH))
        self.page.append(lambda: self.canvas.restoreState())

    def __str__(self):
        """ 
        >>> from reportlab.lib.pagesizes import letter
        >>> canvas = Canvas("lambdatest.pdf", pagesize=letter)
        >>> cfg = {'font': 'Courier', 'fontSize': 10.0, 'kerning': 11.0, 'leftMargin': 0.875, 'canvas': canvas}
        >>> testText = "Statement 1 of 2"
        >>> page = PdfPage(1, cfg, True)
        >>> page.setStatementCount(testText)
        >>> page.__str__()
        'page 1'
        >>> canvas.save()
        """
        for func in self.page:
            func()
        return f"page {self.pageNumber}"

class PostScriptPage(Page):
    # Configuration dict currently must contain font, fontsize, and kerning.
    def __init__(self, pageNumber:int, configs:dict, debug=False):
        super().__init__(pageNumber, configs, debug)
        self.registration = ''
        if self.debug:
            self.registration = f"pageborder"
            self.page.append(f"%!PS-Adobe-3.0")
            self.page.append(f"/{self.font} findfont")
            self.page.append(f"{str(self.fontSize)} scalefont")
            self.page.append(f"setfont")
            self.page.append(self.__registration_functions__())
            self.page.append(f"%%Pages: 1")
        self.page.append(f"%%Page: {str(pageNumber)} {str(pageNumber)}")
        self.isIncomplete = True # marker that page is complete.
        
    # Writes a line of text to the location given. Origin (0,0) is at the
    # bottom left of the page for both PS and PDF.
    # param:  line - string to be laid out on the page
    # param:  x - x coordinate of the string.
    # param:  y - y coordinate.
    # param: bold:bool - True if bold text to be used and false otherwise. 
    # param: fontSize:float - Optional if provided will set font size.  
    # return: y coordinate of the next line of text. 
    def __set_text__(self, line:str, x:float, y:float, bold:bool=False, fontSize:float=None) ->float:
        line = super().__set_text__(line, x, y, bold, fontSize)
        myFontSize = self.fontSize
        if fontSize or bold:
            self.page.append(f"gsave")
            if fontSize:
                myFontSize = fontSize
            if bold:
                self.page.append(f"/{self.font}-Bold findfont")
                self.page.append(f"{str(myFontSize)} scalefont")
                self.page.append(f"setfont")
        x_s = str(x * INCH)
        y_s = str(y * INCH)
        # sanitize the line parens are special symbols in PS.
        line = line.replace('(', '\(')
        line = line.replace(')', '\)')
        self.page.append(f"newpath")
        self.page.append(f"{x_s} {y_s} moveto")
        self.page.append(f"({line}) show")
        if fontSize or bold:
            self.page.append(f"grestore")
        return y - (self.kerning / INCH) # convert points to inches to keep y in sync
    
    # Sets a list of strings at the appropriate location
    # param:  lines - array of strings to be laid out on the page
    # param:  x - x coordinate of the first line of the array of strings. The first
    #         placement is based on the bottom left corner of the first character of the first
    #         line. In Postscript bottom refers to the lowest point on a non-decending character.
    # param:  y - y coordinate with origin (0,0) at the lower left corner of the page.
    # return: float - the y location of the last line printed.
    def __set_text_block__(self, lines:list, x:float, y:float, bold:bool=False) ->float:
        if bold:
            self.page.append(f"gsave")
            self.page.append(f"/{self.font}-Bold findfont")
            self.page.append(f"{str(self.fontSize)} scalefont")
            self.page.append(f"setfont")
        for line in lines:
            y = self.__set_text__(line, x, y)
        if bold:
            self.page.append(f"grestore")
        return y

    # Default method that stringifies object.
    # param:  
    # return: the postscript string of this object.
    def __str__(self):
        if self.debug:
            self.page.append(self.registration)
        self.page.append(f"showpage")
        return '\n'.join(self.page)

    # Adds folds, perferations, and registration marks for debugging. 
    def addRegistrationMarks(self):
        return f"pageborder"

    def __registration_functions__(self) ->str:
        myFunc = '''/inch {
    72.0 mul
} def
/perfline {
    [6 3] 3 setdash
    stroke
    newpath
} def
/fineperfline {
    gsave
    0.5 setgray
    [4 2] 0 setdash
    stroke
    grestore
    newpath
} def
/pageborder {
    % Outline of the page
    0.5 inch 0  inch moveto
    0.5 inch 11 inch lineto
    8   inch 0  inch moveto
    8   inch 11 inch lineto
    0.5 setlinewidth
    perfline
    % Lowest perferation line
    0   inch 3.09375 inch moveto
    8.5 inch 3.09375 inch lineto
    0.25 setlinewidth
    fineperfline
    % Fold line lower 1/3
    0   inch 3.5625 inch moveto
    8.5 inch 3.5625 inch lineto
    perfline
    % Fine perforation above fold lower fold line.
    0   inch 4.09375 inch moveto
    8.5 inch 4.09375 inch lineto
    fineperfline
    % Fine perferation below top fold line.
    0   inch 6.84375 inch moveto
    8.5 inch 6.84375 inch lineto
    fineperfline
    % Top fold line
    0   inch 7.275  inch moveto
    8.5 inch 7.275  inch lineto
    perfline
    % Top-most tear line perferation.
    0   inch 10.4375    inch moveto
    8.5 inch 10.4375    inch lineto
    fineperfline
} def'''
        return myFunc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # Then do the Postscript page tests. 
    doctest.testfile("page.tst")
    print(f"Done, check files")

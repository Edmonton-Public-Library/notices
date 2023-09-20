#!/usr/bin/env python 
###########################################################################
#
#    Copyright (C) 2012 - 2023 Andrew Nisbet, Edmonton Public Library
# The Edmonton Public Library respectfully acknowledges that we sit on
# Treaty 6 territory, traditional lands of First Nations and Metis people.
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
# Purpose: Formatter object. This object brokers information from Customer
# to a location on a page, dependant on the underlying requirement of 
# the type of output you are creating. Formatter is a interface, the
# real work happens in the subclasses that take care of set of the whole
# report, the coordination of the pagination and placement data on a 
# notice and any clean up required to create a well formed output document.
#
# Author:  Andrew Nisbet, Edmonton Public Library
# Date:    November 7, 2012
# Rev:     
#          1.0 - Added licensing changes and pre-referral report processing.
#          0.0 - Dev.
###########################################################################
from datetime import date
from page import PostScriptPage, PdfPage
from page import INCH
from customer import Customer
import sys
try:
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.units import inch
    from reportlab.lib.pagesizes import letter
except:
    errMsg = '''
    Missing reportlib library. It's used to write PDFs. This application
    was written and tested agains version 4.0.x. Install it locally using
    the following sequence of commands.
    0) python -m venv venv
    1) . venv/bin/activate
    2) pip install reportlab
    or alternatively
    1) python -m pip install reportlab
    '''
    print(f"*error:\n{errMsg}")
    sys.exit(-1)

SENTINAL = '#PICKUP_LIBRARY#'
AUTHOR = 'Edmonton Public Library'
WARNING_MSG = ["This file contains personal information about customers of Edmonton Public Library",
    "This information is protected by EPL's FOIP policy, and must NOT be distributed with expressed",
    "permission from the management of EPL."]

class NoticeFormatter:
    # Base class constructor. NoticeFormatter is an abstract class. Use sub-classes 
    # PostScriptFormatter and PdfFormatter.
    # param: fileBaseName:str - File path and name of the output file type without '.ps' or '.pdf'. 
    # param: configs:dict - Dictionary of minimal settings for outputting both PDF and PS. Values
    #   the dictionary should contains are 'font', 'fontSize', 'kerning', and 'leftMargin'. 
    # param: reportDate:str - This allows you to overwrite the default today's date. This is useful
    #   when you are reprinting a report other than the one produced today. 
    # param: debug:bool - Turns on debugging information. Default is 'True'. 
    def __init__(self, fileBaseName:str, 
      configs:dict={'font': 'Courier', 'fontSize': 10.0, 'kerning': 12.0, 'leftMargin': 0.875}, 
      reportDate:str=None, debug:bool=True):
        self.debug           = debug
        if reportDate:
            self.today       = reportDate
        else:
            self.today       = date.today().strftime("%A, %B %d, %Y")
        self.title           = '' # text string for title
        self.header          = [] # text string for header
        self.footer          = [] # text strings for footer
        self.customers       = []
        self.customerNotices = []
        self.fileBaseName    = fileBaseName
        self.configDict      = configs
        self.font            = self.configDict.get('font')
        if not self.font:
            self.font = 'Courier'
            print(f"Using default font value '{self.font}'")
        self.fontSize        = self.configDict.get('fontSize') # points
        if not self.fontSize:
            self.fontSize = 10.0
            print(f"Using default fontSize value '{self.fontSize}'")
        self.kerning         = self.configDict.get('kerning')  # points
        if not self.kerning:
            self.kerning = 11.0
            print(f"Using default kerning value '{self.kerning}'")
        self.blockSpacing    = self.kerning / INCH     # inches
        self.leftMargin      = self.configDict.get('leftMargin') # inches
        if not self.leftMargin:
            self.leftMargin = 0.875
            print(f"Using default leftMargin value '{self.leftMargin}'")
        self.isPdfOutput     = False

    # Outputs the notices to a single either PS or PDF file.
    # Override is required in all subclasses.
    def outputNotices(self):
        pass

    # Sets the customer data to be printed to the final notices.
    # Formats customers into multi-sheet notices if necessary.
    # Customers must be valid customers.
    def setCustomer(self, customer):
        self.customers.append(customer)
        
    # Sets the title in the output file. Only one title is allowed
    # param: text:str - Title text.  
    def setGlobalTitle(self, text:str):
        self.title = text
    
    # Sets the header that all customers in this report will receive. 
    # param: text:str - Title text which is put on a list. 
    def setGlobalHeader(self, text:str):
        self.header.append(text)
        
    # Sets the footer that all customers in this report will receive. 
    # param: text:str - Footer text which is put on a list.
    def setGlobalFooter(self, text:str):
        self.footer.append(text)
    
    # this method actually formats the customers data into pages.
    def format(self):
        # now we are ready to output pages.
        # customerNotices = []
        totalPageCount  = 1
        for customer in self.customers:
            customerPages = []
            # make the customers initial page - they all have at least one.
            page = self.getAdditionalPage(totalPageCount, customer, True)
            customerPages.append(page)
            totalPageCount += 1
            # but if the page was incomplete, create a new one and keep going until it is complete.
            while(page.isIncomplete):
                page = self.getAdditionalPage(totalPageCount, customer)
                customerPages.append(page)
                totalPageCount += 1
            # add the statement page of pages notice
            pageTotal           = len(customerPages)
            customersPageNumber = 1
            customersPageCount  = 0
            for page in customerPages:
                # now we know the total pages for a customer we can output the statement count
                page.setStatementCount('Statement ' + str(customersPageNumber) + ' of '+ str(pageTotal))
                customersPageNumber += 1
                customersPageCount  += 1
                # place the customer notice onto the list of notices.
                self.customerNotices.append(page)
            customer.setPageTotal(customersPageCount)

    # Creates additional pages of a customer notice.
    # param:  pageNumber - Integer, over-all page number used by PS and PDF to deliniate pages.
    # param:  Customer object - is valid and gets printed notices.
    # param:  isFirstPage - True if the call is for the first page of multi-page customer notice and False otherwise.
    # return: A Page object in valid Postscript.
    def getAdditionalPage(self, pageNumber, customer, isFirstPage=False):
        if self.isPdfOutput:
            page = PdfPage(pageNumber, self.configDict, debug=self.debug)
        else:
            page = PostScriptPage(pageNumber, self.configDict, debug=self.debug)
        # every page gets these
        page.setTitle(self.title)
        page.setAddress(customer.getAddress())
        page.setStatementDate('Statement produced: ' + str(self.today)) 
        yPos = page.yDate- self.blockSpacing
        # Each customer gets only one header message so set that now
        if isFirstPage:
            # This code replaces what ever is defined as a sentinal with the customer's pickup library.
            header = []
            if len(customer.header) > 0:
                for line in self.header:
                    header.append(line.replace(SENTINAL, customer.header))
            else:
                header = self.header
            if len(header) > 0:
                yPos = page.setItem(header, self.leftMargin, yPos) - self.blockSpacing
        # Output all the items for a customer
        while (customer.hasMoreItems()):
            item = customer.getNextItem()
            if not page.isRoomForItem(item, yPos):
                customer.pushItem(item)
                return page # we have to make another page to fit it all.
            yPos = page.setItem(item, self.leftMargin, yPos) - self.blockSpacing
        # Add any footer the customer has, usually a bill summary.
        if customer.hasFooter():
            item = customer.getFooter()
            if page.isRoomForItem(item, yPos) == False:
                customer.pushFooter(item)
                return page # we have to make another page to fit it all.
            yPos = page.setItem(item, self.leftMargin, yPos) - self.blockSpacing
        # Add the page's footer
        if page.isRoomForItem(self.footer, yPos):
            page.setItem(self.footer, self.leftMargin, yPos) # This sets the page complete flag.
            page.finalize()
        return page

class PdfFormatter(NoticeFormatter):
    def __init__(self, fileBaseName:str, configs:dict={}, reportDate=None, debug=True):
        # This is a little convoluted, but create the PDF canvas object and add it to the 
        # config dict. This doesn't disturb the PS code and doesn't need the implementor 
        # to know anything about the details of how we do PDF.
        pdfFile = f"{fileBaseName}.pdf"
        # reportlib default page size is A4 so change it to match Ghostscript's default: US Letter. 
        self.canvas = Canvas(pdfFile, pagesize=letter)
        self.canvas.setAuthor(f"Created for {AUTHOR}")
        warning = ' '.join(WARNING_MSG)
        self.canvas.setSubject(f"{warning}")
        configs['canvas'] = self.canvas
        super().__init__(fileBaseName, configs=configs, reportDate=reportDate, debug=debug)
        self.canvas.setTitle(f"Report for {self.today}")
        self.isPdfOutput = True

    # Finalizes all the pages into a single PS file.
    # return: None, but outputs the PDF file.
    def outputNotices(self):
        self.canvas.save()

    def __str__(self):
        return 'PDF formatter: ' + self.fileName

class PostScriptFormatter(NoticeFormatter):
    def __init__(self, fileBaseName:str, configs:dict={}, reportDate=None, debug=True):
        super().__init__(fileBaseName, configs=configs, reportDate=reportDate, debug=debug)

    # Finalizes all the pages into a single PS file.
    # return: 
    def outputNotices(self):
        myFile = open(self.fileBaseName + '.ps', 'w')
        myFile.write('%!PS-Adobe-3.0\n')
        # Tell the PS file how many pages in total there will be
        myFile.write('%%Pages: ' + str(len(self.customerNotices)) + '\n')
        myFile.write(f"%% Created for {AUTHOR} {str(self.today)}\n")
        for warning in WARNING_MSG:
            myFile.write(f"%% {warning}\n")
        myFile.write('%%EndComments\n')
        myFile.write('/' + self.font + ' findfont\n' + str(self.fontSize) + ' scalefont\nsetfont\n')
        for page in self.customerNotices:
            myFile.write(str(page))  
        myFile.close()
        
    def __str__(self):
        return 'PostScript formatter: ' + self.fileName
    
# Initial entry point for program
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    baseFileName = 'testformatpage'
    configs = {'font': 'Courier', 'fontSize': 10.0, 'kerning': 12.0, 'leftMargin': 0.875}
    ### Test Postscript notice formatter. 
    noticeFormatter = PostScriptFormatter(f"{baseFileName}PS", configs, debug=True)
    noticeFormatter.setGlobalTitle(f"Test Page")
    noticeFormatter.setGlobalHeader(f"Our records indicate that the following amount(s) is outstanding by more than 15 days.")
    noticeFormatter.setGlobalHeader(f"This may block your ability to borrow or to place holds or to renew materials online ")
    noticeFormatter.setGlobalHeader(f"or via our telephone renewal line. Please go to My Account at")
    # This is broken to fit - PDF just wraps long lines.
    noticeFormatter.setGlobalHeader(f"http://www.epl.ca/myaccount for full account details.")
    c = Customer()
    customer = c.__create_customer__()
    noticeFormatter.setCustomer(customer)
    noticeFormatter.format()
    noticeFormatter.outputNotices()
    print('=>' + str(customer.getPagesPrinted()))
    ### Test the PDF notice formatter. 
    noticeFormatter = PdfFormatter(f"{baseFileName}PDF", configs, debug=True) 
    noticeFormatter.setGlobalTitle(f"Test Page")
    noticeFormatter.setGlobalHeader(f"Our records indicate that the following amount(s) is outstanding by more than 15 days.")
    noticeFormatter.setGlobalHeader(f"This may block your ability to borrow or to place holds or to renew materials online ")
    noticeFormatter.setGlobalHeader(f"or via our telephone renewal line. Please go to My Account at http://www.epl.ca/myaccount for full account details.")
    c = Customer()
    customer = c.__create_customer__()
    noticeFormatter.setCustomer(customer)
    noticeFormatter.format()
    noticeFormatter.outputNotices()
    print('=>' + str(customer.getPagesPrinted()))
    print(f"Test files:\n {baseFileName}PS.ps\n {baseFileName}PDF.pdf")
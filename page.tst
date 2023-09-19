All Page implementers need to be able to do the following.
* setTitle
* setAddress
* setStatementDate
* setItem
* isRoomForItem
* finalize
* setStatementCount

But all these methods depend on these two internal methods.


>>> from page import PostscriptPage, PdfPage


Tests for PostscriptPage __set_text__()
---------------------------------------
>>> cfg = {'font': 'Courier', 'fontSize': 10.0, 'kerning': 11.0, 'leftMargin': 0.875}
>>> page = PostscriptPage( 1, cfg, True )
>>> page.__set_text__("Hello World", 0.75, 4.5)
4.347222222222222
>>> print(f"{page}")
/Courier findfont
10.0 scalefont
setfont
%%Pages: 1
%%Page: 1 1
newpath
54.0 324.0 moveto
(Hello World) show
showpage

Tests for PostscriptPage __set_text_block__()
---------------------------------------------
>>> msgThreeLines = ['Our records indicate that the following amount(s) is outstanding by more than 15 days.',  
... 'This may block your ability to borrow or to place holds or to renew materials online or via our',
... 'telephone renewal line. Please go to My Account at http://www.epl.ca/myaccount for full account details.']
>>> msgOneLine = ['Statement produced: Friday, August 24 2012']
>>> page = PostscriptPage( 1, cfg, True )
>>> nextLine = page.__set_text_block__( msgOneLine, 0.875, 9.875, True )
>>> textBlock = page.__break_lines__(msgThreeLines)
>>> print(f"{textBlock}")
['Our records indicate that the following amount(s) is outstanding by more than 15', 'days. This may block your ability to borrow or to place holds or to renew materials', 'online or via our telephone renewal line. Please go to My Account at', 'http://www.epl.ca/myaccount for full account details.']
>>> page.__set_text_block__(msgThreeLines, 0.875, (nextLine - 0.18))
8.931111111111107
>>> print(f"{page}")
/Courier findfont
10.0 scalefont
setfont
%%Pages: 1
%%Page: 1 1
gsave
/Courier-Bold findfont
10.0 scalefont
setfont
newpath
63.0 711.0 moveto
(Statement produced: Friday, August 24 2012) show
grestore
newpath
63.0 687.04 moveto
(Our records indicate that the following amount\(s\) is outstanding by more than 15) show
newpath
63.0 676.04 moveto
(days. This may block your ability to borrow or to place holds or to renew materials) show
newpath
63.0 665.0399999999998 moveto
(online or via our telephone renewal line. Please go to My Account at) show
newpath
63.0 654.0399999999997 moveto
(http://www.epl.ca/myaccount for full account details.) show
showpage

Tests for PostscriptPage setTitle
------------------------------------------------
>>> testText = "Title Text"
>>> page = PostscriptPage(1, cfg, True)
>>> page.setTitle(testText)
>>> print(f"{page}")
/Courier findfont
10.0 scalefont
setfont
%%Pages: 1
%%Page: 1 1
gsave
/Courier-Bold findfont
18.0 scalefont
setfont
newpath
238.5 733.5 moveto
(Title Text) show
grestore
showpage


Tests for PostscriptPage setAddress
------------------------------------------------
>>> testText = ["Billy Bishop", "12345 67 Street", "Edmonton, Ab", "T6G 0H4" ]
>>> page = PostscriptPage(1, cfg, True)
>>> page.setAddress(testText)
>>> print(f"{page}")
/Courier findfont
10.0 scalefont
setfont
%%Pages: 1
%%Page: 1 1
newpath
234.0 126.0 moveto
(Billy Bishop) show
newpath
234.0 115.0 moveto
(12345 67 Street) show
newpath
234.0 104.00000000000001 moveto
(Edmonton, Ab) show
newpath
234.0 93.00000000000003 moveto
(T6G 0H4) show
showpage

Tests for PostscriptPage setStatementDate
------------------------------------------------
>>> testText = "Statement produced: Friday, August 24 2012"
>>> page = PostscriptPage(1, cfg, True)
>>> page.setStatementDate(testText)
>>> print(f"{page}")
/Courier findfont
10.0 scalefont
setfont
%%Pages: 1
%%Page: 1 1
newpath
63.0 711.0 moveto
(Statement produced: Friday, August 24 2012) show
showpage


Tests for PostscriptPage setItem
------------------------------------------------
>>> testText = [f"  1   The lion king 1 1/2 [videorecording] / [directed by Kristen J. Sollée].", '      Raymond, Bradley.', '      date billed: 10/23/2012   bill reason: OVERDUE      amt due:     $1.60']
>>> page = PostscriptPage(1, cfg, True)
>>> textBlock = page.__break_lines__(testText)
>>> nextLine = page.setItem(textBlock, 0.875, (nextLine -0.18))
>>> print(f"{page}")
/Courier findfont
10.0 scalefont
setfont
%%Pages: 1
%%Page: 1 1
gsave
/Courier-Bold findfont
10.0 scalefont
setfont
newpath
63.0 687.04 moveto
(  1   The lion king 1 1/2 [videorecording] / [directed by Kristen J. Sollée].) show
newpath
63.0 676.04 moveto
(      Raymond, Bradley.) show
newpath
63.0 665.0399999999998 moveto
(      date billed: 10/23/2012   bill reason: OVERDUE      amt due:     $1.60) show
grestore
showpage


Tests for PostscriptPage isRoomForItem
------------------------------------------------
>>> testText = [f"  1   The lion king 1 1/2 [videorecording] / [directed by Kristen J. Sollée].", '      Raymond, Bradley.', '      date billed: 10/23/2012   bill reason: OVERDUE      amt due:     $1.60']
>>> page = PostscriptPage(1, cfg, True)
>>> textBlock = page.__break_lines__(testText)
>>> page.isRoomForItem(textBlock, 9.8)
True
>>> page.isRoomForItem(textBlock, 0.75)
False


Tests for PostscriptPage setStatementCount
------------------------------------------------
>>> testText = "Statement 1 of 2"
>>> page = PostscriptPage(1, cfg, True)
>>> page.setStatementCount(testText)
>>> print(f"{page}")
/Courier findfont
10.0 scalefont
setfont
%%Pages: 1
%%Page: 1 1
newpath
63.0 324.0 moveto
(Statement 1 of 2) show
showpage

Create a test PS file to convert and compare with 
the PDF generated by the PdfPage class.
=================================================
>>> from reportlab.pdfgen.canvas import Canvas
>>> from reportlab.lib.pagesizes import letter
>>> testPdfFile = "testpagePDF.pdf"
>>> canvas = Canvas(testPdfFile, letter)
>>> # Configuration dict currently must contain font, fontsize, kerning, and leftmargin.
>>> configs = {
...   'font': 'Courier', 
...   'fontSize': 10.0, 
...   'kerning': 11.0, 
...   'leftMargin': 0.875, 
...   'canvas': canvas}
>>> page = PdfPage(1, configs, True)
>>> nextLine = page.__set_text_block__( ['Name Here', 'Address line one', 'Address line two', 'Address line Three', 'P0S 7A1'], 4, 1.75 )
>>> # page.setAddress( ['Name Here', 'Address line one', 'Address line two', 'Address line Three', 'P0S 7A1'])
>>> msg = 'Statement produced: Friday, August 24 2012'
>>> page.setStatementDate(msg)
>>> msg = ['Our records indicate that the following amount(s) is outstanding by more than 15 days.',  
... 'This may block your ability to borrow or to place holds or to renew materials online or via our',
... 'telephone renewal line. Please go to My Account at http://www.epl.ca/myaccount for full account details.']
>>> myBlock = page.__break_lines__( msg )
>>> # print(myBlock)
>>> nextLine = page.__set_text_block__(myBlock, page.xHeader, page.yHeader)
>>> special = "\u00e9"
>>> # special = "\u00d8" # This is the 'O' with strike-through. Python says character maps to undefined. 
>>> msg = [f"  1   The lion king 1 1/2 [videorecording] / [directed by Kristen J. Sollée {special}].",
... '      Raymond, Bradley.',
... '      $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $1.60']
>>> nextLine = page.setItem( textBlock, 0.875, (nextLine - 0.18) )
>>> page.setTitle( 'Test Title' )
>>> canvas.save()


PostscriptPage output for conversion and comparison.
----------------------------------------------------

>>> page = PostscriptPage( 1, configs, True ) 
>>> page.__set_text_block__( ['Name Here', 'Address line one', 'Address line two', 'Address line Three', 'P0S 7A1'], 4, 1.75, True )
0.9861111111111115
>>> msg = ['Statement produced: Friday, August 24 2012']
>>> nextLine = page.__set_text_block__( msg, 0.875, 9.875, True )
>>> msg = ['Our records indicate that the following amount(s) is outstanding by more than 15 days.',  
... 'This may block your ability to borrow or to place holds or to renew materials online or via our',
... 'telephone renewal line. Please go to My Account at http://www.epl.ca/myaccount for full account details.']
>>> myBlock = page.__break_lines__( msg )
>>> # print(myBlock)
>>> nextLine = page.setItem( myBlock, 0.875, (nextLine - 0.18) )
>>> special = "\u00e9"
>>> # special = "\u00d8" # This is the 'O' with strike-through. Python says character maps to undefined. 
>>> msg = [f"  1   The lion king 1 1/2 [videorecording] / [directed by Kristen J. Sollée {special}].",
... '      Raymond, Bradley.',
... '      $<date_billed:3>10/23/2012   $<bill_reason:3>OVERDUE      $<amt_due:3>     $1.60']
>>> nextLine = page.__set_text_block__( msg, 0.875, (nextLine - 0.18), True )
>>> page.setTitle( 'Test Title' )
>>> page.__set_text__('Statement 1 of 2', 0.875, 4.5 )
4.347222222222222
>>> # encoding = 'iso8859_2'
>>> encoding = 'utf_8'
>>> testPsFile = "testpagePS.ps"
>>> with open(testPsFile, encoding=encoding, mode='w') as f:
...     bytesWritten = f.write( str(page) )
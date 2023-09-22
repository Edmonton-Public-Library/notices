All Page implementers need to be able to do the following.
* setTitle
* setAddress
* setStatementDate
* setItem
* isRoomForItem
* finalize
* setStatementCount

But all these methods depend on these two internal methods.


>>> from page import PostScriptPage, PdfPage


Tests for PostScriptPage __set_text__()
---------------------------------------
>>> cfg = {'font': 'Courier', 'fontSize': 10.0, 'kerning': 11.0, 'leftMargin': 0.875}
>>> page = PostScriptPage( 1, cfg, False )
>>> page.__set_text__("Hello World", 0.75, 4.5)
4.347222222222222
>>> print(f"{page}")
%%Page: 1 1
newpath
54.0 324.0 moveto
(Hello World) show
showpage

Tests for PostScriptPage __set_text_block__()
---------------------------------------------
>>> msgThreeLines = ['Our records indicate that the following amount(s) is outstanding by more than 15 days.',  
... 'This may block your ability to borrow or to place holds or to renew materials online or via our',
... 'telephone renewal line. Please go to My Account at http://www.epl.ca/myaccount for full account details.']
>>> msgOneLine = ['Statement produced: Friday, August 24 2012']
>>> page = PostScriptPage( 1, cfg, False )
>>> nextLine = page.__set_text_block__( msgOneLine, 0.875, 9.875, True )
>>> textBlock = page.__break_lines__(msgThreeLines)
>>> print(f"{textBlock}")
['Our records indicate that the following amount(s) is outstanding by more than 15', 'days. This may block your ability to borrow or to place holds or to renew materials', 'online or via our telephone renewal line. Please go to My Account at', 'http://www.epl.ca/myaccount for full account details.']
>>> page.__set_text_block__(msgThreeLines, 0.875, (nextLine - 0.18))
8.931111111111107
>>> print(f"{page}")
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

Tests for PostScriptPage setTitle
------------------------------------------------
>>> testText = "Title Text"
>>> page = PostScriptPage(1, cfg, False)
>>> page.setTitle(testText)
>>> print(f"{page}")
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


Tests for PostScriptPage setAddress
------------------------------------------------
>>> testText = ["Billy Bishop", "12345 67 Street", "Edmonton, Ab", "T6G 0H4" ]
>>> page = PostScriptPage(1, cfg, False)
>>> page.setAddress(testText)
>>> print(f"{page}")
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

Tests for PostScriptPage setStatementDate
------------------------------------------------
>>> testText = "Statement produced: Friday, August 24 2012"
>>> page = PostScriptPage(1, cfg, False)
>>> page.setStatementDate(testText)
>>> print(f"{page}")
%%Page: 1 1
newpath
63.0 711.0 moveto
(Statement produced: Friday, August 24 2012) show
showpage


Tests for PostScriptPage setItem
------------------------------------------------
>>> testText = [f"  1   The lion king 1 1/2 [videorecording] / [directed by Kristen J. Sollée].", '      Raymond, Bradley.', '      date billed: 10/23/2012   bill reason: OVERDUE      amt due:     $1.60']
>>> page = PostScriptPage(1, cfg, False)
>>> textBlock = page.__break_lines__(testText)
>>> nextLine = page.setItem(textBlock, 0.875, (nextLine -0.18))
>>> print(f"{page}")
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


Tests for PostScriptPage isRoomForItem
------------------------------------------------
>>> testText = [f"  1   The lion king 1 1/2 [videorecording] / [directed by Kristen J. Sollée].", '      Raymond, Bradley.', '      date billed: 10/23/2012   bill reason: OVERDUE      amt due:     $1.60']
>>> page = PostScriptPage(1, cfg, False)
>>> textBlock = page.__break_lines__(testText)
>>> page.isRoomForItem(textBlock, 9.8)
True
>>> page.isRoomForItem(textBlock, 0.75)
False


Tests for PostScriptPage setStatementCount
------------------------------------------------
>>> testText = "Statement 1 of 1"
>>> page = PostScriptPage(1, cfg, True)
>>> page.setStatementCount(testText)
>>> print(f"{page}")
%!PS-Adobe-3.0
/Courier findfont
10.0 scalefont
setfont
/inch {
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
} def
%%Pages: 1
%%Page: 1 1
newpath
63.0 324.0 moveto
(Statement 1 of 1) show
pageborder
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
... '      date_billed: 10/23/2012   bill_reason: OVERDUE      amt_due:     $1.60']
>>> nextLine = page.setItem( textBlock, 0.875, (nextLine - 0.18) )
>>> page.setTitle( 'Test Title' )
>>> page.setStatementCount('Statement 1 of 1')
>>> print(page)
page 1
>>> canvas.save()


PostScriptPage output for conversion and comparison.
----------------------------------------------------

>>> page = PostScriptPage( 1, configs, True ) 
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
>>> # special = "\u00d8" # This is the 'O' with strike-through. Python says character maps to undefined. 
>>> msg = [f"  1   The lion king 1 1/2 [videorecording] / [directed by Kristen J. Sollée].",
... '      Raymond, Bradley.',
... '      date_billed: 10/23/2012    bill_reason: OVERDUE      amt_due:     $1.60']
>>> nextLine = page.__set_text_block__( msg, 0.875, (nextLine - 0.18), True )
>>> page.setTitle( 'Test Title' )
>>> page.__set_text__('Statement 1 of 1', 0.875, 4.5 )
4.347222222222222
>>> # encoding = 'iso8859_2'
>>> encoding = 'utf_8'
>>> testPsFile = "testpagePS.ps"
>>> with open(testPsFile, encoding=encoding, mode='w') as f:
...     bytesWritten = f.write( str(page) )
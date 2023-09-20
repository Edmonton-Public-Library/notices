


Tests for reportreader.py including all reports

>>> from reportreader import Hold, Overdue, Bill, PreReferral, PreLost 

Holds
-----
>>> report = Hold('tests/hold.prn', 'tests/bulletin', 'tests/print')
>>> report.parseReport()
True
>>> print(f"{report}")
Hold Notice using: tests/hold.prn
["address: ['Georgia I Grant', '11227 58 Avenue', 'Edmonton, AB', 'T6H 1C3'], snail: True, wellformed: True, itemcount: 4"]

Lost
----
>>> report = PreLost('tests/lost.prn', 'tests/bulletin', 'tests/print')
>>> report.parseReport()
True
>>> print(f"{report}")
PreLost Notice using: tests/lost.prn
["address: ['Arbry Adult', '1234 5678 Saskatchewan DR NW', 'Edmonton, AB', 'T6T 4R7'], snail: True, wellformed: True, itemcount: 2"]

Pre-referral
------------
>>> report = PreReferral('tests/refr.prn', 'tests/bulletin', 'tests/print')
>>> report.parseReport()
True
>>> print(f"{report}")
PreReferral Notice using: tests/refr.prn
["address: ['Jacqueline Onasis', '403-12345 Saskatchewan Drive NW', 'Edmonton, AB', 'T6E 4R9'], snail: False, wellformed: True, itemcount: 2", "address: ['Some customer', '25-1655 49 Street NW', 'Edmonton, AB', 'T6L 2R8'], snail: True, wellformed: True, itemcount: 4"]


Bills
-----
>>> report = Bill('tests/bill.prn', 'tests/bulletin', 'tests/print')
>>> report.parseReport()
True
>>> print(f"{report}")
Bill Notice using: tests/bill.prn
["address: ['Be Kinder Lee', '14220 23 St NW', 'Edmonton, AB', 'T5Y 1N1'], snail: True, wellformed: True, itemcount: 3", "address: ['Barn A Burner', '15005 60 Street NW', 'Edmonton, AB', 'T5A 1Z6'], snail: True, wellformed: True, itemcount: 1", "address: ['Warren Beaty', '111-11636 102 Avenue NW', 'Edmonton, AB', 'T5K 0R4'], snail: True, wellformed: True, itemcount: 12"]

Overdues
--------
>>> report = Overdue('tests/odue.prn', 'tests/bulletin', 'tests/print')
>>> report.parseReport()
True
>>> print(f"{report}")
Overdue Notice using: tests/odue.prn
["address: ['Arbry Adult', '1234 5678 Saskatchewan DR NW', 'Edmonton, AB', 'T6T 4R7'], snail: True, wellformed: True, itemcount: 2"]
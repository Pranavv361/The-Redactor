#Libraries Used
from redactor import redact_names, redact_dates, redact_addresses, redact_genders, redact_phones

#Testing Redact names
def test_redact_names():
     res, redacted = redact_names("Joe Biden is the current US president.")
     #breakpoint()     
     assert res == '█████████ is the current US president.'
     assert redacted == [('Joe Biden', 0, 9)]

#Testing Redact dates
def test_redact_dates():
     res, redacted = redact_dates("Joe Biden became the current US president on 10 Jan 2017.")
     #breakpoint()
     assert res == 'Joe Biden became the current US president on ███████████.'
     assert redacted == [('10 Jan 2017', 45, 56)]

#Testing Redact Addresses
def test_redact_addresses():
     res, redacted = redact_addresses("He stays in Norman, Oklahoma Unites States.")
     #breakpoint()     
     assert res == 'He stays in ██████, ████████ Unites States.'
     assert redacted == [('Norman', 12, 18), ('Oklahoma', 20, 28)]

#Testing Redact genders
def test_redact_genders():
     res, redacted = redact_genders("He will be the president.")
     #breakpoint()
     assert res == '██ will be the president.'
     assert redacted == [('He', 0, 2)]

#Testing Redact Phones
def test_redact_phones():
     res, redacted = redact_phones("Current number is 758-676-8888")
     #breakpoint()
     assert res == 'Current number is ████████████'
     assert redacted == [('758-676-8888', 18, 30)]

 
 
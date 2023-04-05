#Libraries Used
from redactor import redact_names, redact_dates, redact_addresses, redact_genders, redact_phones

#Redact names
def test_redact_names():
    #  breakpoint()
     res, redacted = redact_names("Joe Biden is the current US president.")
     
     assert res == '█████████ is the current US president.'
     assert redacted == [('Joe Biden', 0, 9)]
     assert isinstance(str, list )


 
 
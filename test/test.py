#Libraries Used
from redactor import redact_names


#Redact names
def test_redact_names():
    #  breakpoint()
     res, redacted = redact_names("Joe Biden is the current US president.")
     
     assert res == '█████████ is the current US president.'
     assert redacted == [('Joe Biden', 0, 9)]
 
 
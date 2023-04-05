#Libraries Used
import argparse
import os
import glob
import spacy
import re

#Redact character
Redactcharacter = '\u2588'

#Loading spacy model
nlp = spacy.load('en_core_web_sm')

#Redact Names
def redact_names(text):
    doc = nlp(text)
    redacted_names = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            redacted_text = Redactcharacter * len(ent.text)
            text = text.replace(ent.text, redacted_text)
            redacted_names.append((ent.text, ent.start_char, ent.end_char))
    return text, redacted_names

#Redact Dates
def redact_dates(text):
    doc = nlp(text)
    redacted_dates = []
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            redacted_text = Redactcharacter * len(ent.text)
            text = text.replace(ent.text, redacted_text)
            redacted_dates.append((ent.text, ent.start_char, ent.end_char))
    return text, redacted_dates

#Redact Phones
def redact_phones(text):
    phone_pattern = r'\b(?:\+?1[-. ])?\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4})\b|\b(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})\b'
    redacted_phones = []
    for match in re.finditer(phone_pattern, text):
        redacted_phone = (match.group(0), match.start(), match.end())
        text = text[:match.start()] + Redactcharacter * len(match.group(0)) + text[match.end():]
        redacted_phones.append(redacted_phone)
    return text, redacted_phones

#Redact Genders
def redact_genders(text):
    gender_terms = ['male', 'female', 'transgender', 'cisgender','they', 'them','their', 'theirs',
                    'themselves','father','mother']
    pronouns = ['he','she','him', 'her','his','men', 'women']
    redacted_genders = []
    for term in gender_terms:
        redacted_text = Redactcharacter * len(term)
        matches = ([(match.group(0), match.start(), match.end()) for match in re.finditer(rf'(?i){term}', text)])
        for match in matches:
            redacted_term = match[0]
            text = text[:match[1]] + redacted_text + text[match[2]:]
            redacted_genders.append((redacted_term, match[1], match[2]))
    for term in pronouns:
        redacted_text = Redactcharacter * len(term)
        matches = [(match.group(0), match.start(), match.end()) for match in re.finditer(rf'(?i)\b{term}\b', text)]
        for match in matches:
            redacted_term = match[0]
            text = text[:match[1]] + redacted_text + text[match[2]:]
            redacted_genders.append((redacted_term, match[1], match[2]))
    #print(redacted_genders)    
    return text, redacted_genders

#Redact Addresses
def redact_addresses(text):
    doc = nlp(text)
    redacted_addr = []
    for ent in doc.ents:
        if ent.label_ in ['LOC', 'GPE']:
            redacted_text = Redactcharacter * len(ent.text)
            text = text.replace(ent.text, redacted_text)
            redacted_addr.append((ent.text, ent.start_char, ent.end_char))
    return text, redacted_addr

def main(fileExtension, output_folder, stats, redactnames, redactdates, redactphones, redactgenders, redactaddress):
    filename = []
    text = ""
    #Reading multiple files with same File Extension
    for pattern in fileExtension:
        for file_name in glob.glob(pattern):
            filename.append(file_name)
            redacted_terms = []
            with open(file_name,'r') as f:
                text = f.read()
                if redactnames:
                        text, redacted_names = redact_names(text)
                        if redacted_names:
                                redacted_names.append(('names', len(redacted_names)))
                                redacted_terms.extend(redacted_names)
                if redactdates:
                        text, redacted_dates = redact_dates(text)
                        if redacted_dates:
                                redacted_dates.append(('dates', len(redacted_dates)))
                                redacted_terms.extend(redacted_dates)
                if redactphones:
                        text, redacted_phones = redact_phones(text)
                        if redacted_phones:
                                redacted_phones.append(('phones', len(redacted_phones)))
                                redacted_terms.extend(redacted_phones)
                if redactgenders:
                        text, redacted_genders = redact_genders(text)
                        if redacted_genders:
                                redacted_genders.append(('genders', len(redacted_genders)))
                                redacted_terms.extend(redacted_genders)
                if redactaddress:
                        text, redacted_addresses = redact_addresses(text)
                        if redacted_addresses:
                                redacted_addresses.append(('addresses', len(redacted_addresses)))
                                redacted_terms.extend(redacted_addresses)
                #print(redacted_terms)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                output_file_name = os.path.join(output_folder, os.path.splitext(os.path.basename(file_name))[0] + '.redacted')
                with open(output_file_name, 'w', encoding= 'utf-8') as output_file:
                    output_file.write(text)

                #Stats file
                if os.path.exists(os.path.join(stats, stats +'.txt')):
                    with open(os.path.join(stats, stats +'.txt'), 'a', encoding='utf-8') as f:
                        print('Redaction Statistics for file '+ file_name + ' :')
                        f.write('File name:     '+file_name + '\n')
                        for term in redacted_terms:
                            if len(term) == 3:
                                f.write(f'{term[0]}: at index {term[1]}-{term[2]} redacted\n')
                                #print(f'{term[0]}: at index {term[1]} {term[2]} redacted')
                            else:
                                f.write(f'No of {term[0]} redacted are {term[1]}\n\n')
                                #print(f'No of {term[0]} redacted is {term[1]}')
                else:
                    os.makedirs(stats)
                    with open(os.path.join(stats, stats +'.txt'), 'w', encoding='utf-8') as f:
                        print('Redaction Statistics for file '+ file_name + ' :')
                        f.write('File name:     '+file_name + '\n')
                        for term in redacted_terms:
                            if len(term) == 3:
                                f.write(f'{term[0]}: at index {term[1]}-{term[2]} redacted\n')
                                #print(f'{term[0]}: at index {term[1]} {term[2]} redacted')
                            else:
                                f.write(f'No of {term[0]} redacted are {term[1]}\n\n')
                                #print(f'No of {term[0]} redacted is {term[1]}')


if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Redact sensitive information from text files')
        parser.add_argument('--input', type=str, nargs='+',help='input file pattern', required=True)
        parser.add_argument('--names', action='store_true', help='redact names')
        parser.add_argument('--dates', action='store_true', help='redact dates')
        parser.add_argument('--phones', action='store_true', help='redact phone numbers')
        parser.add_argument('--genders', action='store_true', help='redact genders')
        parser.add_argument('--address', action='store_true', help='redact addresses')
        parser.add_argument('--output', type=str, help='output directory', required=True)
        parser.add_argument('--stats', type=str, choices=['stdout', 'stderr'], default='stdout', help='output statistics to stdout or stderr')

        args = parser.parse_args()

#To access input arguments as attributes of the `args` object
        input_pattern = args.input
        redactnames = args.names
        redactdates = args.dates
        redactphones = args.phones
        redactgenders = args.genders
        redactaddress = args.address
        output_dir = args.output
        stats_output = args.stats

        if args.input:
                main(input_pattern, output_dir, stats_output, redactnames, redactdates, redactphones, redactgenders, redactaddress)
import requests
import re

S = requests.Session()

URL = "https://en.wikiquote.org/w/api.php"

PARAMS = {
    "action": "parse",
    "page": "Jean-Paul Sartre",
    "format": "json",
    "prop": "text"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

#print(DATA["parse"]["text"]["*"])
# get initial quotes 
quotes = re.findall(r"<li>(.*?)\n*<ul>", DATA["parse"]["text"]["*"])

def print_quotes(quotes):
    idx = 1
    for quote in quotes:
        print("quote :  " + str(idx) + " " + quote + "\n")
        idx += 1

# now we need to get rid of strings that are used for page numbers, citations and links 
# first we need to get rid of lines that have p. (basically saying page in book)
quotes = [quote for quote in quotes if not re.search("p. ", quote) ]

# next we need to get rid of strings that have act in them
quotes = [quote for quote in quotes if not re.search("Act [0-9]*", quote) ]

# next we get rid of strings that contain hyperlinks to other pages, might lose some good information but oh well
quotes = [quote for quote in quotes if not re.search("<a\s+href", quote) ]

# still getting rid of links
quotes = [quote for quote in quotes if not re.search("<a\s+rel", quote) ]

# need to get rid of strings with (text) as they are citations
quotes = [quote for quote in quotes if not re.search("\(.*\)", quote) ]


# need to get rid of strings with part in them as they are citations 
quotes = [quote for quote in quotes if not re.search("[Pp]art [0-9]*", quote)]

# get rid of french quotes since we dont want to be mixing french with english
quotes = [quote for quote in quotes if not re.search("<i>", quote)]

# TODO: will need to go back and handle logic for dealing with the section about Jean-Paul Sartre
quotes = [re.sub(r"<.*?>", "", quote) for quote in quotes ]

# will want to get rid of ... pattern, it doesn't really do  anyhting 
quotes = [re.sub(r"\.\.\.", "", quote) for quote in quotes ]

# need to get rid of citation in the format of "Book 2"
quotes = [quote for quote in quotes if not re.search("Book [0-9],", quote) ]

print_quotes(quotes)




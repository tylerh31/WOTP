# (WOTP) Who's on the Pitch?

## About WOTP:

About a month ago I was watching a Barcelona friendly and I couldn't keep up with who was on the pitch. I tried to google who was on the pitch but all I could find was who was subbed on and off but not a list of who was currently on the pitch. 

After some more searching I decided that it probably wouldn't be _too_ hard to make a python script that: 
* gets the starters of a game
* removes and appends to the list depending on subs
* prints a list of who is currently on the pitch


This script **_currently_**: 
* searches the reddit post history of [/u/MatchThreadder/](https://www.reddit.com/u/MatchThreadder/)
* returns a list of the most recent games posted to [/r/soccer](https://www.reddit.com/r/soccer) or [/r/MLS](https://www.reddit.com/r/MLS)
* prompts user which game they want to see **WOTP**
* returns subs made (on and off)
* returns list of who is currently on the pitch for each side

## Requirements:

* bs4
* urllib2
* re
* unicodedata

## Installation:

Simply clone this repo wherever you'd like, install the requirements and simply run "python wotp.py"

## Sample Code!

```python
def get_raw_match_links():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open("http://www.reddit.com/u/MatchThreadder/?limit=50")

    req = urllib2.Request("http://www.reddit.com/u/MatchThreadder/?limit=50", headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")

    # Get all links with class of "bylink comments may-blank" add to links[] list
    for link in soup.find_all('a', class_="bylink comments may-blank"):
        href_pattern = re.compile(ur'.*href="(.*?)/".*')
        comments_link = re.search(href_pattern, str(link)).groups()
        if('/MLS/' in comments_link[0]) or ('/soccer/' in comments_link[0]):
            match_links.append(comments_link[0])
```
## Feedback:

Any feedback is greatly appreciated. 

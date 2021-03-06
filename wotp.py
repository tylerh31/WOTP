#!/usr/bin/python
# -*- coding: latin-1 -*-
# Tyler Hansen 8/1/2016
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import unicodedata

reload(sys)  
sys.setdefaultencoding('utf8')

links = []
match_threads = []
match_links = []

## TODO: Create method for red card and remove from list "/red"

## TODO: Grab minute when substitution was made

## TODO: If player name = 3 grab last 2 not just first one. (dos Santos)

# Take url of requested match and extract info (subs/on the pitch)
def match_thread_info(url):
    team_1_starters = []
    team_2_starters = []
    team_1_subs = []
    team_2_subs = []
    team_1_subbed_in = []
    team_2_subbed_in = []

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)

    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read()

    # MLS and soccer subreddits have different formatting, check to see which link this one is
    if ('/MLS/' in url):
        team_1_starters_subs = get_team_1_name_starters_subs_MLS(html)
        team_2_starters_subs = get_team_2_name_starters_subs_MLS(html)
        match_subs = get_match_subs_MLS(html)
    # If its not MLS its soccer, this is handled in get_raw_match_links
    else:
        team_1_starters_subs = get_team_1_name_starters_subs(html)
        team_2_starters_subs = get_team_2_name_starters_subs(html)
        match_subs = get_match_subs(html)

    team1 = team_1_starters_subs[0]
    starters_team_1 = team_1_starters_subs[1].split(',')
    subs_team_1 = team_1_starters_subs[2].split(',')

    team2 = team_2_starters_subs[0]
    starters_team_2 = team_2_starters_subs[1].split(',')
    subs_team_2 = team_2_starters_subs[2].split(',')

    process_team_starters(starters_team_2, team_2_starters)

    process_team_starters(starters_team_1, team_1_starters)

    process_team_subs(subs_team_1, team_1_subs)

    process_team_subs(subs_team_2, team_2_subs)

    print team1, 'vs.', team2

    for sub in match_subs:
        subOut = sub[0].split(' ')
        # remove empty indexes in subOut
        subOut = filter(None, subOut)
        # for players who only have 1 name (e.g. Kaka)
        if(len(subOut) == 1):
            subOutName = remove_accents(subOut[0])
        elif(len(subOut) == 2):
            subOutName = remove_accents(subOut[1])
        else:
            subOutName = remove_accents(subOut[2])

        subIn = sub[1].split(' ')
        # remove empty indexes in subIn
        subIn = filter(None, subIn)
        # for players who only have 1 name (e.g. Kaka)
        if(len(subIn) == 1):
            subInName = remove_accents(subIn[0])
        elif(len(subIn) == 2):
            subInName = remove_accents(subIn[1])
        else:
            subInName = remove_accents(subIn[2])

        print 'Off:', subOutName, 'On:', subInName

        i = 0
        j = 0

        # buggy with players having more than 2 names.

        for starter in team_1_starters:
            starter = starter.strip()
            starter = starter.split(' ')
            if(len(starter) == 1):
                if(subOutName == starter[0]):
                    del team_1_starters[i]
                    team_1_subbed_in.append(subInName)
            elif(len(starter) == 2):
                if(subOutName == starter[1]):
                    del team_1_starters[i]
                    team_1_subbed_in.append(subInName)
            else:
                if(subOutName == starter[2]):
                    del team_1_starters[i]
                    team_1_subbed_in.append(subInName)
            i += 1

        for starter in team_2_starters:
            starter = starter.strip()
            starter = starter.split(' ')
            if(len(starter) == 1):
                if(subOutName == starter[0]):
                    del team_2_starters[j]
                    team_2_subbed_in.append(subInName)
            elif(len(starter) == 2):
                if(subOutName == starter[1]):
                    del team_2_starters[j]
                    team_2_subbed_in.append(subInName)
                    print subOutName
            else:
                if(subOutName == starter[2]):
                    del team_2_starters[j]
                    team_2_subbed_in.append(subInName)
            j += 1

    team_1_players_on_pitch = team_1_starters + team_1_subbed_in
    team_2_players_on_pitch = team_2_starters + team_2_subbed_in

    print team1, ':', team_1_players_on_pitch
    print team2, ':', team_2_players_on_pitch

def get_team_1_name_starters_subs(html):
    result = re.search('.*<p><a href="#icon-notes-big"></a> <strong>LINE-UPS</strong></p>\s+<p><strong><a href="#\S+"></a>(.*?)</strong></p>\s+<p>(.*?).</p>\s+<p><strong>Subs:</strong>(.*?).</p>', html, re.DOTALL).groups()
    return result
def get_team_2_name_starters_subs(html):
    result = re.search('<p><sup>.*</sup></p>\s+<p><strong><a href="#\S+"></a>(.*?)</strong></p>\s+<p>(.*?).</p>\s+<p><strong>Subs:</strong>(.*?).</p>', html, re.DOTALL).groups()
    return result

def get_match_subs(html):
    result = re.findall('<a href="#icon-sub"></a> Substitution: <a href="#icon-down"></a>(.*?)<a href="#icon-up"></a>(.*?)</p>', html, re.DOTALL)
    return result

def get_team_1_name_starters_subs_MLS(html):
    result = re.search('.*<p><strong>LINE-UPS</strong></p>\s+<p><strong>(.*?)</strong></p>\s+<p>(.*?).</p>\s+<p><strong>Subs:</strong>(.*?).</p>', html, re.DOTALL).groups()
    return result

def get_team_2_name_starters_subs_MLS(html):
    result = re.search('<p><sup>.*</sup></p>\s+<p><strong>(.*?)</strong></p>\s+<p>(.*?).</p>\s+<p><strong>Subs:</strong>(.*?).</p>', html, re.DOTALL).groups()
    return result

def get_match_subs_MLS(html):
    result = re.findall('<a href="/sub-off"></a>(.*?)<a href="/sub-on"></a>(.*?)</p>', html, re.DOTALL)
    return result

def process_team_starters(unprocessed_list, processed_list):
    for starter in unprocessed_list:
        starter = starter.strip()
        starter = remove_accents(starter)
        processed_list.append(starter)

def process_team_subs(unprocessed_list, processed_list):
    for sub in unprocessed_list:
        sub = sub.strip()
        sub = remove_accents(sub)
        processed_list.append(sub)

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

def prompt_user_for_game_link(match_links):
    i = 0
    print 'Available Matches:\n'
    for match_link in match_links:
        processed_match_link = parse_match_link(match_link)
        print i, ':', processed_match_link[0]
        i += 1

    desired_match_link = input("Choose the game you would like to see: ")

    if (desired_match_link not in range(len(match_links))):
        print 'The game you have selected in not in the range of acceptable values, please try again'
        prompt_user_for_game_link(match_links)

    return desired_match_link

def parse_match_link(match_link):
    result = re.search('.*/match_thread_(.*)', match_link, re.DOTALL).groups()
    return result

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', unicode(input_str))
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

get_raw_match_links()
thread = prompt_user_for_game_link(match_links)
match_thread_info(match_links[thread])


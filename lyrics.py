import urllib.request
import re
import string
import time

commonwords = ["the", "a", "and", "to", "for", "of", "in", "you", "i", "me", "it", "we", "be", "on", "my", "your", "all", "no", "im", "was"]

def contains(array, myword):
    for word in array:
        if (word == myword):
            return True
    return False

def intopfives(topfivenums, number):
    for x in range(0, 5):
        if (number > topfivenums[x]):
            return x;
    return -1;

#WIP code - started by Kieran
#The intention is for the user to enter an artist, then it parses out song links from the a-z lyrics website,
#then performs the regular analysis on the words in the songs.

#az-lyrics page lookup by band name - I'm trying to use google results to grab the URL
artist = input("Enter artist name: ")
artist = artist.lower()
artist = re.sub("\d+", "", artist) #remove trailing numbers (well, actually, any numbers, but I haven't devoted enough time to figuring this out right now)
artist = re.sub(r"\s+", '', artist) #get rid of whitespace
if (artist.startswith("the")): #remove leading 'the'
    artist = artist.replace("the", "", 1)
print("Artist: " + artist)
artistLink = "http://www.azlyrics.com/" + artist[0] + "/" + artist + ".html"
print(artistLink)

#get songs urls from the artist page:
songs = []
html = str(urllib.request.urlopen(artistLink).read()).split("<!-- start of song list -->")[1].split("<!-- end of song list -->")[0]
html = html.split("<script type=\"text/javascript\">")[0] #We don't want all of the javascript that generates the html because it is harder to parse.
regex = r"<a href=\"([^\"\']*)\" target=\"_blank\">([^\<\>]*)<\/a>" #matches the specific case of hyperlink that has the song link
matches = re.findall(regex, html)
print(matches)
for t in matches:
    songs.append(t[0].replace("../", "http://www.azlyrics.com/"))
print(songs)

#filename = input("Enter file name: ")
#file = open(filename, 'r')
#songs = file.readlines()

alluniques = []
totaluniques = 0
iterations = 0

for song in songs:
    iterations += 1
    link = song
    print(link)
    html = str(urllib.request.urlopen(link).read()).split("<!-- start of lyrics -->")[1].split("<!-- end of lyrics -->")[0]

    regex = [r"<(.*?)>", r'\\n', r'\\r', r'\\', r'\[(.*?)\]', r'[^\w ]']
    for reg in regex:
        matches = len(re.findall(reg, html))
        if (reg == r'\\n'):
            html = re.sub(reg, " ", html, matches)
        else:
            html = re.sub(reg, "", html, matches)
    words = html.split()

    uniques = []
    for word in words:
        word = word.lower()
        if (contains(uniques, word)):
            for x in range(0, len(uniques)):
                if (uniques[x] == word):
                    uniques[x+1] += 1
        else:
            uniques.extend([word, 1])
            
        if (contains(alluniques, word)):
            for x in range(0, len(alluniques)):
                if (alluniques[x] == word):
                    alluniques[x+1] += 1
        else:
            alluniques.extend([word, 1])

    topfivenums = [0, 0, 0, 0, 0]
    topfivewords = ["", "", "", "", ""]

    for x in range(1, len(uniques), 2):
        index = intopfives(topfivenums, uniques[x])
        if (index != -1):
            if (contains(commonwords, uniques[x-1]) == False):
                topfivenums.insert(index, uniques[x])
                topfivewords.insert(index, uniques[x-1])
                topfivenums.pop(5)
                topfivewords.pop(5)
    print("Total Uniques: " + str(int(len(uniques)/2)))
    totaluniques += int(len(uniques)/2)

    for x in range(0, 5):
        print (topfivewords[x] + " " + str(topfivenums[x]))

    print("\n")
    time.sleep(.5) # don't spam HTTP requests at servers too quickly, they dont like that

print("Average Total Uniques: " + str(totaluniques/iterations))

topfivenums = [0, 0, 0, 0, 0]
topfivewords = ["", "", "", "", ""]

for x in range(1, len(alluniques), 2):
    index = intopfives(topfivenums, alluniques[x])
    if (index != -1):
        if (contains(commonwords, alluniques[x-1]) == False):
            topfivenums.insert(index, alluniques[x])
            topfivewords.insert(index, alluniques[x-1])
            topfivenums.pop(5)
            topfivewords.pop(5)

for x in range(0, 5):
    print (topfivewords[x] + " " + str(topfivenums[x]))


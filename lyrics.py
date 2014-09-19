import urllib.request
import re
import string

commonwords = ["the", "a", "and", "to", "for", "of", "in"]

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

file = open("songs.txt", 'r')
songs = file.readlines()

for song in songs:
    artist = song.split()[0]
    title = song.split()[1]
    link="http://www.azlyrics.com/lyrics/"+artist+"/"+title+".html"
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

    for x in range(0, 5):
        print (topfivewords[x] + " " + str(topfivenums[x]))

    print("\n")

file.close()

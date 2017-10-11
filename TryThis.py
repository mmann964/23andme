#!/usr/bin/python

import requests
import json
import csv

#from urllib2 import Request, urlopen, URLError

def extract_pageCount(jStr):
    try:
        return int(jStr['volumeInfo']['pageCount'])
    except KeyError:
        return 0

def extract_key(myKey, jStr):
    try:
        return int(jStr['volumeInfo'][myKey])
    except KeyError:
        return 0



baseUrlStr = 'https://www.googleapis.com/books/v1/volumes?q='
searchStr = raw_input("what subject are you interested in? ")
#if ' ' in x:  #replace space with '%20'

requestStr = baseUrlStr + searchStr

response = requests.get(requestStr)
print response.status_code
#print response.content
data = response.json()
book = data["items"]
print type(data)
print data["totalItems"]
print type(book)
print "before sort"
print book[0]["volumeInfo"]["pageCount"]
#print book[1]["volumeInfo"]["pageCount"]

#print type(data["items"])
print data["items"][0]["etag"]
#print data["items"][0]["volumeInfo"]["title"]
##sort by price, average rating, rating count, published date, page count
#print data["items"][0]["saleInfo"]["retailPrice"]["amount"]
#print data["items"][0]["volumeInfo"]["averageRating"]
#print data["items"][0]["volumeInfo"]["ratingsCount"]
#print data["items"][0]["volumeInfo"]["publishedDate"]
#print data["items"][0]["volumeInfo"]["pageCount"]


# sort by page count
book.sort(key=extract_pageCount)
#book.sort(key=extract_key(self, 'pageCount'))
#print data["items"][0]["etag"]
print "after sort"
print book[0]["volumeInfo"]["pageCount"]

# how to write the json to csv?
# how to load csv into object?
# how to sort by price, average, rating, rating count, published date, page count

# write to csv
with open('mel.csv', 'wb') as csvfile:
    libwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL )
    for i in book:
        libwriter.writerow([i])
        #print i


## why are there 'u's by all the json strings?
## how do you comma separate objects?  Can they still be readable?

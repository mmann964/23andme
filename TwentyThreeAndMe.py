#!/usr/bin/python

import requests
import json
import csv
import datetime
import calendar


def extract_price(jStr):
    try:
        return int(jStr['saleInfo']['retailPrice']['amount'])
    except KeyError:
        return 0

def extract_rating(jStr):
    try:
        return int(jStr['volumeInfo']['averageRating'])
    except KeyError:
        return 0

def extract_ratingsCount(jStr):
    try:
        return int(jStr['volumeInfo']['ratingsCount'])
    except KeyError:
        return 0

def extract_publishedDate(jStr):
    try:
        dateStr = jStr['volumeInfo']['publishedDate']
        # dateStr is in different formats.
        # figure out which one it is, and convert to sortable timestamp
        if len(dateStr) == 4:
            # assume it's just the year
            formatStr = '%Y'
        elif len(dateStr) == 7:
            # assume it's YYYY-MM
            formatStr = '%Y-%m'
        elif len(dateStr) == 10:
            # assume it's YYYY-MM-DD
            formatStr = '%Y-%m-%d'
        else:
            # not sure -- return 0
            return 0
        d1 = datetime.datetime.strptime(dateStr, formatStr)
        return calendar.timegm(d1.utctimetuple())

        #return time.mktime(time.strptime(dateStr, formatStr))  #doesn't work for dates prior to 1900

    except KeyError:
        return 0

def extract_pageCount(jStr):
    try:
        return int(jStr['volumeInfo']['pageCount'])
    except KeyError:
        return 0

def getSearchStr(prompt="What subject are you interested in? "):
    searchStr = raw_input(prompt)
    return searchStr.replace(' ', '+')

def saveToFile(book_dict, fname):
    with open(fname, 'wb') as csvfile:
        libwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for i in book_dict:
            libwriter.writerow([i])

def getNextChoice():
    # Ask the user what they want to do next

    print ""
    print "Here are your choices: "
    print "\t[Q]uit  "
    print "\tSort by [P]rice"
    print "\tSort by [A]verage rating"
    print "\tSort by [R]ating count"
    print "\tSort by Published [D]ate"
    print "\tSort by Page [C]ount"
    print "\t[S]ave to CSV file"
    print "\t[N]ew search"
    print "\t[L]oad existing file"
    return raw_input("> ").upper()

def doSearch():
    searchStr = getSearchStr()
    requestStr = baseUrlStr + searchStr

    # do the request
    response = requests.get(requestStr)

    # exit if you get a 400 or 500 error
    if response.status_code >= 400:
        print "Exiting."
        print "Your search returned an unexpected response code: " + str(response.status_code)
        exit(response.status_code)

    # put the response into a dictionary called books
    data = response.json()
    return data["items"]  # data is a dictionary, data["items"] is a list of 10 dictionary items

def getBookInfo(book, index):
    try:
        val = book["volumeInfo"][index]
    except KeyError:
        val = "N/A"
    return val

def printResults(books):
    print ""
    for i in range(len(books)):
        title = getBookInfo(books[i], "title")
        pageCount = getBookInfo(books[i], "pageCount")
        avgRating = getBookInfo(books[i], "averageRating")
        ratingCount = getBookInfo(books[i], "ratingsCount")
        publishDate = getBookInfo(books[i], "publishedDate")

        try:
            price = books[i]['saleInfo']['retailPrice']['amount']
        except KeyError:
            price = "N/A"

        print u"Title: {}, Price: {} Pages: {}, Publish Date: {}, Average Rating: {}, Number of Ratings: {}"\
            .format(title, price, pageCount, publishDate, avgRating, ratingCount)

    print ""

if __name__ == "__main__":

    baseUrlStr = 'https://www.googleapis.com/books/v1/volumes?q='

    books = doSearch() #books is a list
    printResults(books)


    # next choices
    while True:
        a = getNextChoice()

        if a == 'Q':
            exit()
        elif a == 'N':
            books = doSearch()
            printResults(books)
        elif a == 'S':
            fname = raw_input("Which file should I save these results to? ")
            if len(fname) == 0:
                print "No filename given.  Saving to temp.csv."
                fname = "temp.csv"
            saveToFile(books, fname)
        elif a == 'P':
            books.sort(key=extract_price)
            printResults(books)
        elif a == 'A':
            books.sort(key=extract_rating)
            printResults(books)
        elif a == 'R':
            books.sort(key=extract_ratingsCount)
            printResults(books)
        elif a == 'D':
            books.sort(key=extract_publishedDate)
            printResults(books)
        elif a == 'C':
            books.sort(key=extract_pageCount)
            printResults(books)
        elif a == 'L':
            print "I haven't been able to make this work."
        else:
            getNextChoice()

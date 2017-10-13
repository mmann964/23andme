#!/usr/bin/python

import requests
import csv
import datetime
import calendar


def extract_price(jsonstr):
    try:
        return float(jsonstr['saleInfo']['retailPrice']['amount'])
    except KeyError:
        return 0


def extract_rating(jsonstr):
    try:
        return float(jsonstr['volumeInfo']['averageRating'])
    except KeyError:
        return 0


def extract_ratings_count(jsonstr):
    try:
        return int(jsonstr['volumeInfo']['ratingsCount'])
    except KeyError:
        return 0


def extract_published_date(jsonstr):
    try:
        datestr = jsonstr['volumeInfo']['publishedDate']
        # dateStr is in different formats.
        # figure out which one it is, and convert to sortable timestamp
        if len(datestr) == 4:
            # assume it's just the year
            formatstr = '%Y'
        elif len(datestr) == 7:
            # assume it's YYYY-MM
            formatstr = '%Y-%m'
        elif len(datestr) == 10:
            # assume it's YYYY-MM-DD
            formatstr = '%Y-%m-%d'
        else:
            # not sure -- return 0
            return 0
        d1 = datetime.datetime.strptime(datestr, formatstr)
        return calendar.timegm(d1.utctimetuple())
    except KeyError:
        return 0


def extract_page_count(jsonstr):
    try:
        return int(jsonstr['volumeInfo']['pageCount'])
    except KeyError:
        return 0


def get_search_str(prompt="What subject are you interested in? "):
    searchstr = ""
    while searchstr == "":
        searchstr = raw_input(prompt).strip()
    return searchstr.replace(' ', '+')


def save_to_file(book_dict, filename):
    try:
        csvfile = open(filename, 'wb')
        libwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for i in book_dict:
            libwriter.writerow([i])
    except IOError:
         print "Error while saving file."   


def get_next_choice():
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
    s = raw_input("> ").strip().upper()
    if len(s) == 0:
        return ""
    else:
        return s[0]


def do_search():
    searchstr = get_search_str()
    requeststr = baseUrlStr + searchstr

    # do the request
    response = requests.get(requeststr)

    # exit if you get a 400 or 500 error
    if response.status_code >= 400:
        print "Exiting."
        print "Your search returned an unexpected response code: " + str(response.status_code)
        exit(response.status_code)

    # put the response into a dictionary called books
    data = response.json()
    try:
        d = data["items"]  # data is a dictionary, data["items"] is a list of 10 dictionary items
    except KeyError:
        d = []  # no results were returned
    return d


def get_book_info(book, index):
    try:
        val = book["volumeInfo"][index]
    except KeyError:
        val = "N/A"
    return val


def print_results(booklist):
    print ""
    for i in range(len(booklist)):
        title = get_book_info(booklist[i], "title")
        page_count = get_book_info(booklist[i], "pageCount")
        avg_rating = get_book_info(booklist[i], "averageRating")
        rating_count = get_book_info(booklist[i], "ratingsCount")
        publish_date = get_book_info(booklist[i], "publishedDate")

        try:
            price = booklist[i]['saleInfo']['retailPrice']['amount']
        except KeyError:
            price = "N/A"

        print u"Title: {}, Price: {} Pages: {}, Publish Date: {}, Average Rating: {}, Number of Ratings: {}"\
            .format(title, price, page_count, publish_date, avg_rating, rating_count)

    print ""


if __name__ == "__main__":

    baseUrlStr = 'https://www.googleapis.com/books/v1/volumes?q='

    books = do_search()  # books is a list
    print_results(books)

    # next choices
    while True:
        a = get_next_choice()

        if a == 'Q':
            exit()
        elif a == 'N':
            books = do_search()
            print_results(books)
        elif a == 'S':
            fname = raw_input("Which file should I save these results to? ").strip()
            if len(fname) == 0:
                print "No filename given.  Saving to temp.csv."
                fname = "temp.csv"
            save_to_file(books, fname)
        elif a == 'P':
            books.sort(key=extract_price)
            print_results(books)
        elif a == 'A':
            books.sort(key=extract_rating)
            print_results(books)
        elif a == 'R':
            books.sort(key=extract_ratings_count)
            print_results(books)
        elif a == 'D':
            books.sort(key=extract_published_date)
            print_results(books)
        elif a == 'C':
            books.sort(key=extract_page_count)
            print_results(books)
        elif a == 'L':
            print "Coming Soon!"

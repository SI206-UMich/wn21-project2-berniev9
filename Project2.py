from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.
    
    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    dic = {}
    f = open(filename,'r')
    soup = BeautifulSoup(f, 'html.parser')
    tbody_list = soup.find_all('tbody')
    for tag in tbody_list:
        a_list = tag.find_all('td',None)
        for a in a_list:
            get_title = a.find_all('a', class_="bookTitle")
            get_auth = a.find_all('a', class_="authorName")
            for b in get_title:
                for c in get_auth:
                    title = b.text.strip()
                    auth = c.text.strip()
                    if not title in dic.keys():
                        dic[title] = auth



    new_lis = [(k, v) for k, v in dic.items()]   
    return new_lis

    


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    new_list = []
    url ='https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table')
    tbody = table.find_all('a', class_="bookTitle")
    for i in range(10):
        text =tbody[i]['href'] 
        new_list.append('https://www.goodreads.com'+ text)

    return new_list


    
def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find('div', id="metacol")
    h1 = div.find('h1', id="bookTitle") 
    title = h1.text.strip()
    a = div.find('a',class_="authorName")
    author =a.text.strip()
    span = div.find('span',itemprop="numberOfPages")
    pages = span.text.strip(' pages')

    new_tuple = (title,author,int(pages))

    return new_tuple



def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    new_list = []
    soup = BeautifulSoup(filepath, "html.parser")
    div = soup.find('div', class_="categoryContainer")
    clear = div.find_all('div', class_="category clearFix")
    for book in clear:
        #category
        categor = book.find('h4')
        categ = categor.text.strip()
        #link
        link = book.find('a')
        link1 = link.get('href',None).strip()
        #Title
        r = requests.get(link1)
        soup2 = BeautifulSoup(r.text,"html.parser")
        title = soup2.find('a', class_="winningTitle choice gcaBookTitle")

        new_tuple = (categ,title.text.strip(),link1)
        new_list.append(new_tuple)

    return new_list
def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.
    
    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......



    This function should not return anything.
    """
    dir = os.path.dirname("search_results.htm")
    outfile = os.path.join(dir,filename)
    f = open(outfile, 'w')
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['Book Title','Author Name'])
    writer.writerows(data)
    f.close()


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls

    def setUp(self):
        self.search_urls = get_search_links()



    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        soup1 = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(soup1), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(soup1),list)
        # check that each item in the list is a tuple
        for i in range(len(soup1)):
            self.assertEqual(type(soup1[i]),tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(soup1[0],('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(soup1[19],('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))


    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(self.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(self.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        for url in self.search_urls:
            self.assertIsInstance(url, str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for i in self.search_urls:
            self.assertTrue(i.startswith('https://www.goodreads.com/book/show/'))



    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for i in self.search_urls:
            summaries.append(get_book_summary(i))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries),10)
        for tup in summaries:
            # check that each item in the list is a tuple
            self.assertIsInstance(tup, tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(tup), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(tup[0]), str)
            self.assertEqual(type(tup[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(tup[2]), int)
            # check that the first book in the search has 337 pages
            self.assertEqual(summaries[0][2],337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        f = open('best_books_2020.htm', 'r')
        r = f.read()
        f.close()
        summary = summarize_best_books(r)
        # check that we have the right number of best books (20)
        self.assertEqual(len(summary),20)
        for item in summary:
            # assert each item in the list of best books is a tuple
            self.assertIsInstance(item, tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(item), 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(summary[0][0], 'Fiction')
        self.assertEqual(summary[0][1], 'The Midnight Library')
        self.assertEqual(summary[0][2], 'https://www.goodreads.com/choiceawards/best-fiction-books-2020')

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(summary[19][0], 'Picture Books')
        self.assertEqual(summary[19][1], 'Antiracist Baby')
        self.assertEqual(summary[19][2], 'https://www.goodreads.com/choiceawards/best-picture-books-2020')


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        results = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(results,'test.csv') 
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        csv_lines = []
        with open('test.csv') as csv_file:
            csvv = csv.reader(csv_file)
            for row in csvv:
                    csv_lines.append(row)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Book Title', 'Author Name'])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[20], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])


if __name__ == '__main__':
    # print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)




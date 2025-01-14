import requests 
import time
from bs4 import BeautifulSoup as bs

class Quote:
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags
    
    def __str__(self):
        return f"{self.text}. \nAuthor: {self.author}. \nTags: {self.tags}"

def main():
    url = "https://quotes.toscrape.com"
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    quotes = scrape_quotes(soup)
    while(True):
        #time.sleep(0.5)
        if get_next_url(soup) is None:
            break
        next_page = url + get_next_url(soup)
        r = requests.get(next_page)
        soup = bs(r.content, "html.parser")
        quotes.extend(scrape_quotes(soup))
    print("Question 1:")
    top_tags(quotes)
    print("Question 2:")
    shortest_quote(quotes)
    print("Question 3:")
    longest_quote(quotes)
    print("Question 4:")
    authors_works(quotes)
    return

def scrape_quotes(soup: bs):
    quotes = soup.find_all("div", {"class": "quote"})
    quotesList = []

    for quote in quotes:
        text = quote.find("span", {"class": "text"}).get_text(strip=True)
        author = quote.find("small", {"class": "author"}).get_text(strip=True)
        tags = quote.find_all("a", {"class": "tag"})
        tags_text = []
        for tag in tags:
            tags_text.append(tag.get_text(strip=True))
        quotesList.append(Quote(text, author, tags_text))

    return(quotesList)

def get_next_url(soup: bs):
    nextUrl = soup.find("li", {"class": "next"})
    if nextUrl is None:
        return None
    anchor = nextUrl.find("a")
    url = anchor['href']
    return(url)

def shortest_quote(quotes):
    shortestQuote = quotes[0]
    for quote in quotes:
        if len(quote.text) < len(shortestQuote.text):
            shortestQuote = quote
    print(f"Shortest quote: {shortestQuote.text} By {shortestQuote.author}")

def longest_quote(quotes):
    longestQuote = quotes[0]
    for quote in quotes:
        if len(quote.text) > len(longestQuote.text):
            longestQuote = quote
    print(f"Longest quote: {longestQuote.text} By {longestQuote.author}")

def top_tags(quotes):
    tagDict = {}
    for quote in quotes:
        for tag in quote.tags:
            if tag not in tagDict:
                tagDict.update({tag: 1})
            else:
                currentCount = tagDict[tag]
                tagDict.update({tag: currentCount+1})
    tagDict = sorted(tagDict.items(), key=lambda x: x[1], reverse=True)
    for i in range(10):
        print(tagDict[i])

def authors_works(quotes):
    authorDict: dict = {}
    multipleWorks: dict = {}
    for quote in quotes:
        author = quote.author
        if author not in authorDict:
            authorDict.update({author: 1})
        else:
            currentCount = authorDict[author]
            authorDict.update({author: currentCount+1})
    for i, j in authorDict.items():
        if j > 1:
           multipleWorks.update({i: j})
    multipleWorks = sorted(multipleWorks.items(), key=lambda x: x[1], reverse=True) 
    for i, j in multipleWorks:
        print(i + ", " + str(j))
        
if __name__ == "__main__":
    main()
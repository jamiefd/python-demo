from bs4 import BeautifulSoup
import requests
from extractor import resultsToDf

def getS1Jobs(keyword, page):

  # Populate url

  url = "https://www.s1jobs.com/jobs/?keywords_required=" + keyword + "&page=" + str(page)

  # Show progress

  print("Fetching page " + str(page))

  # Download the html document
  
  response = requests.get(url).text

  # Parse to text with BeautifulSoup
  
  doc = BeautifulSoup(response, "html.parser")

  # Parse the text object and extract variables for analysis

  df = resultsToDf(doc)

  # Return a data frame
  
  return df
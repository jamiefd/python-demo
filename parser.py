from bs4 import BeautifulSoup

def selectToString(result,css_selector):

  # BeautifulSoup will return lists in the loop, which we can't extract text from, so the selectToString function will help

  # Extract CSS selection target, convert to string and strip []

  s = str(result.select(css_selector)).strip("[]")

  # Parse it back out with BeautifulSoup to text

  s = BeautifulSoup(s, "html.parser").get_text()

  # Return text string
  
  return s
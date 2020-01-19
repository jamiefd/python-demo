import pandas as pd
from parser import selectToString
from datetime import datetime, date
import time

def resultsToDf(doc):
  
  page_df = pd.DataFrame()

  # subset the document to only <div id="results_column">
 
  doc = doc.find("div", {"id": "results_column"} )

  # iterate through the individual results, save to data frame

  for res in doc.find_all("div", class_="row"):
    
    # If H2 is empty (call to action, feature box), then skip
 
    if res.select("div.res a > h2") != []:

      # Job title is in the H2 under div with class res
 
      job_title = selectToString(res,"div.res a > h2")
      
      # Best place to get advertiser is from a strong element only visible on XS displays
 
      advertiser = selectToString(res,"span.visible-xs > strong")
      
      # Location is in a span with class loc
 
      loc = selectToString(res,"span.loc")

      # Salary was reviewed during production. It's apparently a free text field for the advertiser. 
      # There is no consistency. 
      # Sometimes it doesn't appear, sometimes it doesn't contain a number, sometimes it's an hourly rate, sometimes it's a range.
      # We could write rules to parse and handle salaries, but as long as it remains free-text, an edge case will occur. 
      # Something like this would be best handled with a manual cleanup, so we'll skip it for this exercise.
      # We'll extract anyway, because it has an unusual selection path

      # Salary is in a span with a class matching the job's location
      salary = selectToString(res,"span." + loc)

      # Date posted is in span with class date-posted
 
      posted = selectToString(res,"span.date-posted")
 
      # Amend the string to remove 'Date posted '
 
      posted = posted.replace("Date posted: ","")
 
      # Format as a usable date
 
      posted = datetime.strptime(posted,"%d %B")
 
      # Year isn't published, so assume that if date is in the future then it was published last year
      # Subtract 1 from year value if month value is greater than today's month value
 
      if posted.strftime("%m") > date.today().strftime("%m"):
        posted = posted.strftime("%d-%m-" + str(int(date.today().strftime("%Y")) - 1) )
      else:
        posted = posted.strftime("%d-%m-" + str(int(date.today().strftime("%Y"))) )

      # Store values in a dict object
 
      i_dict = {"job":job_title,"by":advertiser,"loc":loc,"date":posted}

      # Convert i_dict to a pandas dataframe
 
      i_df = pd.DataFrame([i_dict])

      # Append to cumulative dataframe
 
      page_df = page_df.append(i_df)
 
    else:
      pass
  
  return page_df
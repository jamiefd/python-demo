# Small set of functions and loops which scrape results from S1Jobs for a chosen keyword, iterate through pages of results and then show some example summarisations

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from browser import getS1Jobs
from datetime import datetime
import time

# URL format
# https://www.s1jobs.com/jobs/?keywords_required=<k>&page=<n>
# Two variables: k = keyword, n = page number

# Set keyword:
# What are we going to search for?

keyword = "python"

# Initialise a data frame

df = pd.DataFrame()

# Initialise n_results for the loop

n_results = True

# Loop until S1 jobs stops returning results
# Start on page 1

p = 1

while n_results != 0:

  # Get results for keyword

  result = getS1Jobs(keyword, p)

  # Check number of rows in result object
  ## 0 for rows, 1 for cols

  n_results = result.shape[0]

  # Append results to data frame

  df = df.append(result)

  # Increment page number

  p = p + 1

# How many jobs did we find?

print(len(df.index))

## Where are the jobs?

# First, group the df by location, counting each job

where = df.groupby(["loc"], as_index=False)["job"].count()

# Then, plot with location on the x axis and count of job on the y

where_plot = sns.barplot(x = "loc", y = "job", data = where)

# Set some axis labels
where_plot.set(xlabel = "Location", ylabel = "Number of " + keyword + " job listings")

# Set the chart title
where_plot.set_title(keyword + " job listings on S1jobs.com on " + datetime.today().strftime("%d %B %Y"))

# Save the chart to a png in the working directory
where_plot.get_figure().savefig("where-are-jobs-located.png")

## Who is advertising the roles?
# First, group the df on by (advertiser), counting each job

who = df.groupby(["by"], as_index=False)["job"].count()

# Then, sort by greatest to least. No visualisation for this one, table is best for long categorical lists like this.

who = who.sort_values(by = ["job"] , ascending = False)

print(who)

# Word profiling, which words are common in job titles

# First, let's clean the data, removing some commonly used symbols and stop words which aren't useful in the analysis

chars_to_remove = ["!","£","$","%","^","&","*","-","_","=",")","(","[","]","{","}","~","@",":",";","/","?",">",",","<","|"]

for char in chars_to_remove:
  df["job"] = df["job"].str.replace(char,"")

# Some symbols are left, as they are legitimate. e.g. C#, C++, .NET etc.

# Set the column to lowercase

df["job"] = df["job"].str.lower()

# Initialise a list

titles_list = []

# Iterate through rows the data
# Range of 0 to last row will iterate through all rows

for row in range(0,len(df.index)):

  # Convert value to string, then split on whitespace
  # Access by index, iterate rows, always column 0

  job_words = df.iloc[row,0].split(" ")

  # Append the strings to the list

  titles_list.append(job_words)

  # Increment row number

  row = row + 1

# Flatten the word list of lists

flat_word_list = []

# Iterate through each list

for sublist in titles_list:

  # Go into each list nest and append the items to the flat_word_list

    for item in sublist:
        flat_word_list.append(item)

# Make this a dataframe for grouping later

words = pd.DataFrame(flat_word_list)

# Give the columns sensible names, and add a count for summing

words.columns = ["word"]
words["count"] = 1

# Group by word, to get a count of appearances

wordgroup = words.groupby(["word"], as_index = False)["count"].sum()

# Sort high to low, to see most popular words

wordgroup = wordgroup.sort_values(by = ["count"] , ascending = False)

# Drop invalid rows (there's often non-printing spaces creeping in)

wordgroup = wordgroup[wordgroup["word"] != ""]

# Let's look at the whole dataframe

print(wordgroup.to_string())
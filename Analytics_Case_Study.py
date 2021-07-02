#!/usr/bin/env python
# coding: utf-8

# # Option 2: Data Engineering Case Study
# Since we are working with a stringified table, I thought that pandas would be a great tool to wangle and clean the table.

# In[1]:


# Importing libraries
import pandas as pd
from io import StringIO


# In[2]:


# Setting stringified table
data = StringIO('Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n')


# In[3]:


# Reading table
flights = pd.read_csv(data, ";")
flights.head()


# #### 1. FlightCodes column: Some values are null. Flight Codes are supposed to increase by 10 with each row so 1010 and 1030 will have 1020 in the middle. Fill in these missing numbers and make the column an integer column (instead of a float column).
# 

# In[4]:


# Fill NA values in FlightCodes, increasing by 10
flights["FlightCodes"] = flights["FlightCodes"].interpolate(method='linear', order=10)
# Changing FlightCodes column to integer
flights = flights.astype({"FlightCodes":'int'})
flights.head()


# In[5]:


display(flights.dtypes)


# #### 2. To_From column: Should be split into two separate columns for better analysis! Split on '_' to create two new columns respectively. Also, the case of the column is not very readable, convert the column into capital case.
# 
# I noticed that "NEWYORK" in the dataset has no space because of the way the table was formatted. This may cause issues in the future if other data is referring to the city of New York in another format (e.g New York).

# In[6]:


# Split To_From into two new columns
flights[['To','From']] = flights["To_From"].str.split("_",expand=True)
# Drop To_From
flights.drop(columns =["To_From"], inplace = True)
# Change all cities to uppercase
flights['To'] = flights['To'].str.upper()
flights['From'] = flights['From'].str.upper()
flights.head()


# #### 3. Airline Code column: Clean the  Airline Codes to have no punctuation except spaces in the middle. E.g. '(Porter Airways.)' should become 'Porter Airways'.
# 
# While the case study did not call for this, I also removed the numbers associated with Air France for data consistency. I feel that the '12' does not add any value and does not conform with the rest of the column's formatting. It could just be referring to a particular flight route but I would reach out to stakeholders\data consumers to confirm.

# In[7]:


# Remove all punctuations
flights["Airline Code"] = flights['Airline Code'].str.replace('[^\w\s]','')
# Remove all numbers
flights["Airline Code"] = flights["Airline Code"].str.replace('\d+', '')
# Remove any leading/trailing whitespace
flights["Airline Code"] = flights["Airline Code"].str.strip()
flights.head()


# #### 4. Write a mock SQL query on the above table to find all flights leaving from Waterloo.

# In[ ]:



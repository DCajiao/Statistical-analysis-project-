# It is the main cleaning process to start the analysis.
# Libraries
import numpy as np
import pandas as pd
import re
# Load the dataset
df1 = pd.read_csv("../dataset/USA_CA.csv", encoding="latin1")
df2 = pd.read_csv("../dataset/USA_TX.csv", encoding="latin1")
df3 = pd.read_csv("../dataset/USA_PA.csv", encoding="latin1")
# Merge data sets into one data set
df = pd.concat([df1, df2, df3], ignore_index=True)

#START THE CLEANING PROCESS
# drop null values
df = df.dropna()
#----------------------------------------------------------------
#Defining a function to extract numbers from a string
def extract_numbers(text): 
    numbers = re.findall(r'\d+', str(text))  # Find all digit groups
    numbers = ''.join(numbers)                # Converts the numbers found to a string
    return numbers
#Use function to fix wrong numeric data types

# Paid_Work_Hours
# Work_At_Home_Hours
# Importance_reducing_pollution
# Sleep_Hours_Non_Schoolnight

df["Paid_Work_Hours"] = pd.to_numeric(df["Paid_Work_Hours"].apply(extract_numbers)) # Fix the column 'Paid_Work_Hours'
df["Work_At_Home_Hours"] = pd.to_numeric(df["Work_At_Home_Hours"].apply(extract_numbers)) # Fix the column 'Work_At_Home_Hours'
df["Importance_reducing_pollution"] = pd.to_numeric(df["Importance_reducing_pollution"].apply(extract_numbers)) # Fix the column 'Importance_reducing_pollution'
df["Sleep_Hours_Non_Schoolnight"] = pd.to_numeric(df["Sleep_Hours_Non_Schoolnight"].apply(extract_numbers)) # Fix the column 'Sleep_Hours_Non_Schoolnight'
#----------------------------------------------------------------

#EXPORT THE MERGED, CLEAN DATASET WITH ADJUSTED DATA TYPES# Exporting the DataFrame to a CSV file
df.to_csv('../dataset/datasetcleaned.csv', index=False)
#----------------------------------------------------------------
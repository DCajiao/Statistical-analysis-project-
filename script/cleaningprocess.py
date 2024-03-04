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
#First module cleaning of ranges and characters
def clean_ranges_and_text(value:str, option:int=1):
    """This module clean the ranges and return the lowest or bigest value depends wich option chosse the user 
    1) for the bigest
    2) for the lowest number
    """
    try:
        value = str(value)
    except:
        pass
    def identify_range_pd_series(value:str, option):
        option = option==1
        def this_is_a_range_value(obje:str, option=option):
            pattern = r"(\d+)-(\d+)"
            try:
                coincide = re.match(pattern, obje)
            except:
                return obje
            if coincide:
                if option:
                    return coincide.group(2)
                return coincide.group(1)
            return obje
        x = this_is_a_range_value(value)
        return x
    
    def identify_float_pd_series(value):
        def this_is_a_float_value(obje:str):
            pattern = r"(\d+)[.](\d+)"
            pattern2 = r"(\d+)\s*\D"
            try:
                coincide = re.match(pattern, obje)
                coincide2 = re.match(pattern2, obje)
            except:
                return obje
            if coincide or coincide2:
                if coincide:
                    return coincide.group(0)
                return coincide2.group(1)
            return obje
        x = this_is_a_float_value(value)
        return x
    
    value = identify_range_pd_series(value,option)
    value = identify_float_pd_series(value)
    return value

#Second module change of types for use in a series
def change_type(value):
    try:
        value = float(value)
    except:
        pass
    return value

#Use function to fix wrong numeric data types

# Paid_Work_Hours
# Work_At_Home_Hours
# Importance_reducing_pollution
# Sleep_Hours_Non_Schoolnight

df["Paid_Work_Hours"] = df["Paid_Work_Hours"].apply(clean_ranges_and_text) # Fix the column 'Paid_Work_Hours'
df["Paid_Work_Hours"] = df["Paid_Work_Hours"].apply(change_type)
df["Work_At_Home_Hours"] = df["Work_At_Home_Hours"].apply(clean_ranges_and_text) # Fix the column 'Work_At_Home_Hours'
df["Work_At_Home_Hours"] = df["Work_At_Home_Hours"].apply(change_type)
df["Importance_reducing_pollution"] = df["Importance_reducing_pollution"].apply(clean_ranges_and_text) # Fix the column 'Importance_reducing_pollution'
df["Importance_reducing_pollution"] = df["Importance_reducing_pollution"].apply(change_type)
df["Sleep_Hours_Non_Schoolnight"] = df["Sleep_Hours_Non_Schoolnight"].apply(clean_ranges_and_text) # Fix the column 'Sleep_Hours_Non_Schoolnight'
df["Sleep_Hours_Non_Schoolnight"] = df["Sleep_Hours_Non_Schoolnight"].apply(change_type)
#----------------------------------------------------------------

#EXPORT THE MERGED, CLEAN DATASET WITH ADJUSTED DATA TYPES# Exporting the DataFrame to a CSV file
df.to_csv('../dataset/datasetcleaned.csv', index=False)
#----------------------------------------------------------------
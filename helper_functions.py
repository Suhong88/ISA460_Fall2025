# create a function to display sample records by a group of columns
import numpy as np
import pyspark.sql.functions as F
import pyspark.sql.types as T

def displayByGroup(df, group_size, sample_size=5):
    column_split=np.array_split(df.columns, len(df.columns)//group_size)
    for X in column_split:
        df.select(*X).show(sample_size,False)
        
def columnsLowerCase(df):
    return df.toDF(*[x.lower() for x in df.columns])        

# based on a list of orderd numbers, calculate the avg, max and min
# change between the two consecutive numbers 
@F.udf(T.MapType(T.StringType(), T.DoubleType()))
def changeStats(list):
    change_list=[]
    total_days=len(list)

    for i in range(0, total_days-1):
        current_value=list[i]
        next_value=list[i+1]
        value_diff=abs(next_value-current_value)
        change_list.append(value_diff)
    
    avgChange=round(sum(change_list)/len(change_list),2)
    maxChange=round(max(change_list),2)
    minChange=round(min(change_list),2)
    return {'avgChange': avgChange, 'maxChange': maxChange, 'minChange':minChange}

def sanitizeColumnName(name):
    """Drops unwanted characters from the column name.
 
    We replace spaces, dashes and slashes with underscore,
    and only keep alphanumeric characters.
    """
    answer = name
    for i, j in ((" ", "_"), ("-", "_"), ("/", "_"), ("&", "and")):   
        answer = answer.replace(i, j)
    return "".join(
        [
            char
            for char in answer
            if char.isalpha() or char.isdigit() or char == "_"       
        ]
    )
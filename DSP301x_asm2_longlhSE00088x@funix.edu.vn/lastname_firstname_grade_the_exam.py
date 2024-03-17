#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: dragonsave
"""

import pandas as pd
import numpy as np

try:  
    # Task 1
    # Enter the number of class
    num_of_class = input("Enter number of class: ")
    no_class = f"class{num_of_class}.txt"
    
    # Task 2
    # Open file
    with open(no_class) as f:
        f.seek(0)
        print(f"Open sucessful file of class {num_of_class}")
        lines = f.readlines()
        print("----ErrorLines------")
        list_of_valited_lines = []
        valid_lines = 0
        
        # Check the validity of the data
        for i, line in enumerate(lines):
            line = line.strip()
            x = line.split(",")
            
            # The data must has 26 values
            if len(x) != 26:
                print("The data line is invalid: insufficient number of values")
                print(line)
                
            # The student code must start with N   
            elif not x[0].startswith('N') or len(x[0]) != 9:
                    print("The data line is invalid: wrong form of student code")
                    print(line)
            else:
                valid_lines += 1
                list_of_valited_lines.append(x)
                
                        
    invalid_lines = len(lines) - valid_lines 
    print("-------Summary---------")
    
    # Print out the result
    if invalid_lines != 0:
        print(f"The number of students is: {len(lines)}")            
        print(f"The number of valid lines is {valid_lines}")  
        print(f"The number of invalid lines is {invalid_lines}")  
    else:
        print("No error found!")
        score = 0
    
    # Task 3
    # correct answer 
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
    answer_key = answer_key.split(",")
    
    print("-----ScoreAnalysis----------")
    valid_data = pd.DataFrame(list_of_valited_lines)
    valid_data = valid_data.set_index(0)  
    
    list_of_score = []
    
    # Calculating the score for students
    for l in valid_data.iloc:
        score = 0
        for x, key in zip(l, answer_key):
            if x == key:
                score += 4 # Correct answer
            elif x == '':
                score += 0  # Omitted answer
            else:
                score -= 1  # Wrong answer
        list_of_score.append(score) 
     
    student_valid_number = len(valid_data.iloc[:,0])
    score_raw = []
    score_raw = {"Student Code" : valid_data.index ,"Total score" : list_of_score}
    score_table = pd.DataFrame(score_raw)
    print(score_table)
    
    # Finding the highest skip questions
    highest_miss_value = 0.1
    most_skip = []
    for l in range(25):
        num_miss = len([n for n in valid_data.iloc[:,l] if (n == "")])
        if num_miss > highest_miss_value:
            highest_miss_value = num_miss
            most_skip = [valid_data.columns[l]]
        elif num_miss == highest_miss_value:
            most_skip.append(valid_data.columns[l])
        else:
            pass
    
    # Finding the highest wrong questions
    highest_wrong_value = 0.1
    most_wrong = []
    for l in range(25):
        num_wrong = len([n for n in valid_data.iloc[:,l] if (n != "" and n != answer_key[l])])
        if num_wrong > highest_wrong_value:
            highest_wrong_value = num_wrong
            most_wrong = [valid_data.columns[l]]
        elif num_wrong == highest_wrong_value:
            most_wrong.append(valid_data.columns[l])
        else:
            pass
        
    # Calculating wrong percentage 
    percentage_wrong = round((highest_wrong_value/student_valid_number)*100,3)
    print(f"*The most wrong question(s) in class {num_of_class} is/are: ")
    print(f"  question(s) {most_wrong[0:]} with {highest_wrong_value} times which accounted for {percentage_wrong} percentage")
    
    # Calculating skip percentage 
    percentage_skip = round((highest_miss_value/student_valid_number)*100,3)
    print(f"*The most skip question(s) in class {num_of_class} is/are: ")
    print(f"  question(s) {most_skip[0:]} with {highest_miss_value} times which accounted for {percentage_skip} percentage")
    
    print("------------Summary---------------")
    print("*List of students had score greater than 80")
    print(score_table[score_table["Total score"] > 80])
    print("*Mean Score: ", round(score_table["Total score"].mean(),3))
    print("*Standard deviation: ", round(score_table["Total score"].std(),3))
    print("*Max Score: ", round(score_table["Total score"].max(),3))
    print("*Min Score: ", round(score_table["Total score"].min(),3))
    print("*Range Score: ", score_table["Total score"].max()-score_table["Total score"].min())
    print("*Mode: ", round(score_table["Total score"].mode(),3))
    
    # Task 4
    
    print("--------ExportGradesFile--------------")
    
    # Creating new result file for each class
    file_name = f"class{num_of_class}_grades.txt"
    with open(file_name, "w") as new_file:
        for i in range(len(score_raw["Student Code"])):
            line = f"{score_raw['Student Code'][i]},{score_raw['Total score'][i]}\n"
            new_file.writelines(line)
    print("Export successful")

except FileNotFoundError:
    print("Sorry, I can't find this filename. Please re-enter")
except Exception as e:
    print(f"An error occurred: {e}")

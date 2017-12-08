# -*- coding: utf-8 -*-
"""
KNN Implementation

@author: 100525709, Adwan Salahuddin Syed
"""
#------------------------------------------------------------------------------- 
# 
import csv
import math
import random

def standardizeInput(dataset):
    """
    standardizeInput(dataset)
    
    This function normalizes and preprocesses a dataset before analysis
    
    @arg dataset    Dataset to be standardized
    
    @return Standardized dataset
    """
    
    # Importing Training Data
    importedCSV = csv.reader(open(dataset))
    importedCSV.__next__() #Discard headings
    list = []

    minimums = [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999]
    maximums = [0,0,0,0,0,0,0,0,0]
    
    # Attach numeric labels
    for row in importedCSV:
        if row[0] == 'boy':
            row[0] = 0
        elif row[0] == 'girl':
            row[0] = 1
    
        if row[3] == 'Urban':
            row[3] = 0
        elif row[3] == 'Suburban':
            row[3] = 0.5
        elif row[3] == 'Rural':
            row[3] = 1
    
        if row[8] == 'Grades':
            row[8] = 0
        elif row[8] == 'Sports':
            row[8] = 0.5
        elif row[8] == 'Popular':
            row[8] = 1

        for i in range (len(row)):
            row[i] = float(row[i])
    
            if row[i] < minimums[i]:
                minimums[i] = row[i]
            if row[i] > maximums[i]:
                maximums[i] = row[i]
    
        list.append(row)
    

    #Normalize the values
    for row in list:
        for i in range(len(row)):
            row[i] = (row[i] - minimums[i])/(maximums[i] - minimums[i])
            
    return list
    
def euclideanDistance(test,training):
    """
    euclideanDistance(test, training)
    
    This function finds the euclidean distances from test row
    against entire training dataset
    
    @arg test       Test row
    @arg training   Training dataset
    
    @return List of euclidean distances
    """
    total_distances = []
    sum = 0
    
    for row in training:
        edistance = []
        
        # distance function
        for i in range(0,len(row)):
            sum += math.pow((test[i] - row[i]),2)
            edistance.append(math.sqrt(sum))
            
        total_distances.append(edistance)
    
    return (total_distances)
    
def k_nearest_neighbors(dataset, test_item, k):
    """
    k_nearest_neighbors(dataset, test_item, k)
    
    This function finds the nearest neighbor distances
    
    @arg dataset        Training dataset
    @arg test_item      Test row
    @arg k              Randomly selected K value
    
    @return Nearest neighbor distances
    """
    if len(dataset) <= k:
        print("K is set to a value greater than dataset")
        
    # Finds all neighbor distances
    neighbors = euclideanDistance(test_item,dataset)
    
    # Totals distances before finding nearest neighbor
    distances = []
    for row in neighbors:
        total = 0
        for i in range(0,len(row)):
            total += row[i]
        distances.append(total)
    
    # Using insertion sort finds nearest K distances (neighbors)
    ordered_distances = insertionSort(distances)   
    nearest_distances = []
    for i in range(0,k):
        nearest_distances.append(ordered_distances[i])
    
    return nearest_distances
    
def checkAccuracy(nearest_neighbors, training, test):
    """
    checkAccuracy(nearest_neighbors, training, test)
    
    This function finds the accuracy of the test row in question
    against the training set
    
    @arg nearest_neighbors      Nearest neighbor distances
    @arg training               Training dataset
    @arg test                   Test row
    
    @return Percentage of accuracy
    """
    nearest_neighbor_accuracy = []
    
    for nearest in nearest_neighbors:
        
        # Find positioning of nearest neighbors
        sum = 0
        correctness = 0
        total_distances = []
        for row in training:
            edistance = []
    
            for i in range(0,len(row)):
                sum += math.pow((test[i] - row[i]),2)
                edistance.append(math.sqrt(sum))
            total_distances.append(edistance)
            
        for d in total_distances:

            total = 0
            for i in range(0,len(d)):
                total += d[i]
            
            # If nearest neighbor found calculate accuracy against test row
            if total == nearest:
                
                # Find accuracy of individual columns of test row
                accuracy_columns = []
                for i in range(0,len(row)):
                    correctness = float(test[i]/(row[i]+.1))
                    accuracy_columns.append(correctness/len(row)*100)
                
                # Total test row column accuracies into percentage
                percentages_total = 0 
                for i in range(0,len(row)):
                    percentages_total += accuracy_columns[i]
        
        # Average percentage of nearest neighbors
        avg_percentage = percentages_total/len(row)
        nearest_neighbor_accuracy.append(avg_percentage)
    
    # Calculate percentage accuracy of all neighbors
    neighbor_totals = 0
    for i in range(0,len(nearest_neighbor_accuracy)):
        neighbor_totals += nearest_neighbor_accuracy[i]
    
    final_accuracy = neighbor_totals/len(nearest_neighbor_accuracy)
    
    return final_accuracy

def insertionSort(list):
    """
    insertionSort(list)
    
    This function uses insertion sort algorithm to order a list
    
    @arg list   List of integers
    
    @return Ordered list
    """
    # Algorithm for insertion sort
    for j in range(1,len(list)):
        key = list[j]
        i = j - 1
        while (i >= 0) and (list[i] > key):
            list[i + 1] = list[i]
            i = i - 1
        list[i + 1] = key 

    return list
    
def randomK():
    # generate random value of K between 3 and 10
    k = random.randint(3,10)
    
    return k
#------------------------------------------------------------------------------- 
#   
training_set = 'SchoolkidsTrain.csv'
test_set = 'SchoolkidsTest.csv'
    
stdtraining = standardizeInput(training_set)
stdtest = standardizeInput(test_set)

#Tester Program
count = 0
for row in stdtest:
    k = randomK()
    nearest_neighbors = k_nearest_neighbors(stdtraining, row, k)
    percentage = checkAccuracy(nearest_neighbors, stdtraining, row)
    count += 1
    print ("\nTest set row[%d]:" % count)
    print ("K value: %d" % k)
    print ("Accuracy: %d %%" % percentage)
    


    



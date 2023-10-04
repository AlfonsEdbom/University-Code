# -*- coding: utf-8 -*-
# Written by Alfons Edbom Devall <alde0033@student.umu.se>.
# May be used by the course coordinator in the course 5DV150 (Python) at Umeå University
# Usage exept those listed above requires permission by the author.
"""
Reads a file provided by the user and asks the user how the list should be sorted

The file given by the user should be a text file containing a floating point number per line

"""

from ListAsTwoCell import List

def ListLength(lst):
    """
    Purpose: Returns the length of the list
    Parameters: lst - A list
    Returns: The number of elements present in the list as a integer
    Comment: Returns 0 if the list is empty
    """
    counter = 0
    pos = lst.first()
    while pos != lst.end():
        counter += 1
        pos = lst.next(pos)
    
    return counter

def printDLL(lst):
    """
        Purpose: Prints each element in a list, starting with the first element.
        Parameters: lst - A list
        Returns: -
        Comment: 
    """        
    p = lst.first()
    #Prints each line
    while p != lst.end():
        print(lst.inspect(p))
        p = lst.next(p)
    print()

def ListSplit(lst):
    """
        Purpose: Splits a list into 2 halves
        Parameters: lst - A list
        Returns: lList - List containing the left/first half of lst
                 rList - List containing the right/second half of lst
        Comment: If odd number of elements in list, rList contains 1 more element than lList
    """
    #Finds where the middle of list is to cut
    mid = ListLength(lst) // 2
    pos = lst.first()
    
    lList = List()
    lpos = lList.end()
    
    rList = List()
    rpos = rList.end()
    
    #Creates lList
    for i in range(0, mid):
        v = lst.inspect(pos)
        lList.insert(lpos, v)
        
        pos = lst.next(pos)
        lpos = lList.end()
    #Creates rList
    while pos != lst.end():
        v = lst.inspect(pos)
        rList.insert(rpos, v)
        
        pos = lst.next(pos)
        rpos = rList.end()
    
    return lList, rList


def LowToHigh(S1, S2):
    """
        Purpose: Returns True if the first element in list S1 is less than or equal to the first element in S2
        Parameters: S1 - A list
                    S2 - A list
        Returns: True if first element is less in S1 than in S2, else returns False
        Comment: 
    """            
    less = False
    if S1.inspect(S1.first()) <= S2.inspect(S2.first()):
        less = True

    return less

def HighToLow(S1, S2):
    """
        Purpose: Returns True if the first element in list S1 is larger than or equal to the first element in S2
        Parameters: S1 - A list
                    S2 - A list
        Returns: True if first element is larger in S1 than in S2, else returns False
        Comment: 
    """            
    greater = False
    if S1.inspect(S1.first()) >= S2.inspect(S2.first()):
        greater = True
    
    return greater

def mergesort(S, comparefunc):
    """
        Purpose: To sort a list 
        Parameters: S - A list
                    comparefunc - A function that compares the first elements in 2 lists
        Returns: A sorted list
        Comment: Depending on comparefunc can return a list sorted in both ascending and descending order
        
        Inspired from F5 DoA
    """  
    
    if ListLength(S) > 1:
        
        #Creates two halves of the list
        (S1, S2) = ListSplit(S)
        
        #Recursive call on each half
        S1 = mergesort(S1, comparefunc)
        S2 = mergesort(S2, comparefunc)
        
        #Merge the 2 halves
        S = merge(S1, S2, comparefunc)
    
    return S

def merge(S1, S2, comparefunc):
    """
        Purpose: Merges two lists into a sorted list
        Parameters: S1 - A list
                    S2 - A list
                    comparefunc - A function that compares the first elements in 2 lists
        Returns: A sorted list
        Comment: Depending on comparefunc can return a list sorted in both ascending and descending order
    """                
    
    S = List()
    
    while not S1.isempty() and not S2.isempty():
        
        if comparefunc(S1, S2):
            #comparefunc is True
            S.insert(S.end(), S1.inspect(S1.first()))
            S1.remove(S1.first())
            
        else:
            #comparefunc is False
            S.insert(S.end(), S2.inspect(S2.first()))
            S2.remove(S2.first())
            
    while not S1.isempty():
        #Moves the rest of S1 into S
        S.insert(S.end(), S1.inspect(S1.first()))
        S1.remove(S1.first())
    
    while not S2.isempty():
        #Moves the rest of S2 into S
        S.insert(S.end(), S2.inspect(S2.first()))
        S2.remove(S2.first())
    
    return S

""" Main program starts here """

aList = List()

file_name = input("Name of file to be read: ")
floatFile = open(file_name, 'r') 

#Inserts value converted to float to last position in aList
pos = aList.end()
for line in floatFile:
    aList.insert(pos, float(line))
    pos = aList.end()
    
floatFile.close()

print("Hur vill du sortera listan? \nHögt till lågt (1) \nLågt till högt (2) \nAvsluta (q)")
keepGoing = True
while keepGoing:
    
    choice = input("välj 1, 2 eller q: ")
    
    if choice == '1':
        aList = mergesort(aList, HighToLow)
        print("Såhär ser listan ut nu: ")
        printDLL(aList)
    
    elif choice == '2':
        aList = mergesort(aList, LowToHigh)
        print("Såhär ser listan ut nu: ")
        printDLL(aList)
            
    elif choice == 'q':
        print("Du valde att avsluta och såhär ser listan ut nu:  ")
        printDLL(aList)
        keepGoing = False
    
    else:
        print("Not a valid input. Try again!")
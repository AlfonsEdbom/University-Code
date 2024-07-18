# -*- coding: utf-8 -*-
"""Test baserat på pseudokod från föreläsningen F5 s.13 """
from ListAsArray import List

def ListLength(lst):
    #Ger längd på lista
    counter = 0
    pos = lst.first()
    while pos != lst.end():
        counter += 1
        pos = lst.next(pos)
    
    return counter

def printDLL(l):
    #Skriver ut lista
    p = l.first()
    while p != l.end():
        print(l.inspect(p))
        p = l.next(p)
    print()

def ListSplit(lst):
    #Delar i lista i två 
    mid = ListLength(lst) // 2
    pos = lst.first()
    
    lList = List()
    lpos = lList.end()
    
    rList = List()
    rpos = rList.end()
    
    for i in range(0, mid):
        v = lst.inspect(pos)
        lList.insert(lpos, v)
        
        pos = lst.next(pos)
        lpos = lList.end()
    
    while pos != lst.end():
        v = lst.inspect(pos)
        rList.insert(rpos, v)
        
        pos = lst.next(pos)
        rpos = rList.end()
    
    return lList, rList


def LowToHigh(S1, S2):
    #Returns True if first in S1 > S2, else False
    less = False
    if S1.inspect(S1.first()) <= S2.inspect(S2.first()):
        less = True

    return less

def HighToLow(S1, S2):
    #Returns True if V1 < V2, else False
    greater = False
    if S1.inspect(S1.first()) >= S2.inspect(S2.first()):
        greater = True
    
    return greater

def mergesort(someList, comparefunc):
    if ListLength(someList) > 1:
        
        (S1, S2) = ListSplit(someList)
        
        S1 = mergesort(S1, comparefunc)
        S2 = mergesort(S2, comparefunc)
        
        someList = merge(S1, S2, comparefunc)
    
    return someList

def merge(S1, S2, comparefunc):
    
    S = List()
    
    while not S1.isempty() and not S2.isempty():
        
        if comparefunc(S1, S2):
            #Välj vänstra / S1 och lägg till i slutet av S
            S.insert(S.end(), S1.inspect(S1.first()))
            S1.remove(S1.first())
            
        else:
            #Välj högre/ S2 och lägg till i slutet av S
            S.insert(S.end(), S2.inspect(S2.first()))
            S2.remove(S2.first())
            
    while not S1.isempty():
        #Lägger till resterande av S1 i slutet av S
        S.insert(S.end(), S1.inspect(S1.first()))
        S1.remove(S1.first())
    
    while not S2.isempty():
        #Lägger till resterande av S2 i slutet av S
        S.insert(S.end(), S2.inspect(S2.first()))
        S2.remove(S2.first())
    
    return S


""" Main Starts here """

aList = List()

floatFile = open("heltal.txt", 'r') 

#Inserts value converted to float to last position in aList
pos = aList.end()
for line in floatFile:
    aList.insert(pos, float(line))
    pos = aList.end()
    
floatFile.close()


keepGoing = True

print("Såhär ser listan ut nu")
printDLL(aList)

print("Hur vill du sortera listan? \nHögt till lågt (1) \nLågt till högt (2) \nAvsluta (q)")

while keepGoing:
    
    choice = input("välj 1, 2 eller q: ")
    
    if choice == '1':
        bList = mergesort(aList, HighToLow)
        print("Såhär ser listan ut nu: ")
        printDLL(bList)
    
    elif choice == '2':
        cList = mergesort(aList, LowToHigh)
        print("Såhär ser listan ut nu: ")
        printDLL(cList)
            
    elif choice == 'q':
        print("Du valde att avsluta")
        keepGoing = False
    
    else:
        print("Not a valid input. Try again!")
        
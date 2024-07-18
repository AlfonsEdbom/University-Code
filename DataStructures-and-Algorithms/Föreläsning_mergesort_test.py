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
    
    for i in range(0, mid):
        v = lst.inspect(pos)
        lList.insert(lpos, v)
        
        pos = lst.remove(pos)
        lpos = lList.end()
        
    rList = lst
    
    return lList, rList

def LowToHigh(V1, V2):
    #Returns True if V1 > V2, else False
    less = False
    if V1 <= V2:
        less = True
    
    return less

def HighToLow(V1, V2):
    #Returns True if V1 < V2, else False
    greater = False
    if V1 >= V2:
        greater = True
    
    return greater

def mergesort(someList):
    if ListLength(someList) > 1:
        
        (S1, S2) = ListSplit(someList)
        
        S1 = mergesort(S1)
        S2 = mergesort(S2)
        
        someList = merge(S1, S2)
    
    return someList

def merge(S1, S2):
    
    S = List()
    
    while not S1.isempty() and not S2.isempty():
        S1Value = S1.inspect(S1.first())
        S2Value = S2.inspect(S2.first())
        
        if S1Value <= S2Value:
            #Välj vänstra / S1 och lägg till i slutet av S
            S.insert(S.end(), S1Value)
            S1.remove(S1.first())
            
        else:
            #Välj högre/ S2 och lägg till i slutet av S
            S.insert(S.end(), S2Value)
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


printDLL(aList)
bList = mergesort(aList)
printDLL(bList)


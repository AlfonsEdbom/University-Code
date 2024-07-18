from ListAsArray import List
#Ska använda mig utan mergesort!!!!
#Kolla hur ListSplit delar små listor!!!!!

def ListLength(lst):
    #Ger längd på lista
    counter = 0
    pos = lst.first()
    while pos != lst.end():
        counter += 1
        pos = lst.next(pos)
    
    return counter

def ListSplit(lst):
    #Delar i lista i två 
    mid = ListLenth(lst) // 2
    pos = lst.first()
    lList = List()
    lpos = lList.end()
    
    for i in range(0,mid):
        v = lst.inspect(pos)
        lList.insert(lpos, v)
        
        pos = lst.remove(pos)
        lpos = lList.end()
    rList = lst
    return lList, rList


def mergesort(S):
    #Fungerar inte optimalt! Jämför med andra mergeSort!
    
    if ListLength(S) > 1:
        (S1, S2) = ListSplit(S)
        
        mergesort(S1)
        mergesort(S2)
        
        S = merge(S1, S2)
    
    return S

def merge(S1, S2):
    S = List()
    
    while not S1.isempty() and not S2.isempty():
        if S1.inspect(S1.first()) <= S2.inspect(S2.first()):
            S.insert(S.end(), S1.inspect(S1.first()))
            S1.remove(S1.first())
            
        else:
            S.insert(S.end(), S2.inspect(S2.first()))
            S2.remove(S2.first())
            
    while not S1.isempty():
        S.insert(S.end(), S1.inspect(S1.first()))
        S1.remove(S1.first())
    
    while not S2.isempty():
        S.insert(S.end(), S2.inspect(S2.first()))
        S2.remove(S2.first())
    
    return S


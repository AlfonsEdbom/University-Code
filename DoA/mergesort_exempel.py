def mergeSort(myList):
    if len(myList) > 1:
        mid = len(myList) // 2
        left = myList[:mid]
        right = myList[mid:]
        
        
        #Recursive call on each half
        mergeSort(left)
        mergeSort(right)
        
        #two iterators for traversing the two halves
        i = 0
        j = 0
        
        #iterator for the main list
        k = 0 
        
        while i < len(left) and j < len(right):
            print(left[i])
            print(right[i])
            if left[i] <= right[j]:
                #The value from the left half has been used
                print("Left is smaller and left[i] is inserted: ", left[i])
                
                myList[k] = left[i]
                #Move the iterator forward
                i +=1
            else: 
                print("Right is smaller and Right[j] is inserted: ", right[j])
                myList[k] = right[j]
                j += 1
            #Move to the next slot
            k += 1
            
        #For all the remaining values
        while i < len(left):
            print("Right är slut och lägger in resterande av left: ", left[i])
            myList[k] = left[i]
            i += 1
            k += 1
            
        while j < len(right):
            print("Left är slut och lägger in resterande av right: ", right[j])
            myList[k] = right [j]
            j +=1
            k += 1
        print("Såhär ser myList ut nu: ", myList)

myList = [4,3,2,1]
mergeSort(myList)
print(myList)
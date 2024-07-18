from ListAsTwoCell import List

sList = List()

pos = sList.end()

for i in range(1,6):
    sList.insert(pos, i)
    
pos = sList.first()
while pos != sList.end():
    print(sList.inspect(pos))
    pos = sList.next(pos)


print('\n')

aList = List()
pos = aList.end()
count = 10
for i in range(5):
    aList.insert(pos, i)
    count += 1
    print(count)

printDLL(aList)
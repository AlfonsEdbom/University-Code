# -*- coding: utf-8 -*-
# Written by Alfons Edbom Devall <alde0033@student.umu.se>.
# May be used by the course coordinator in the course 5DV150 (Python) at Umeå University
# Usage exept those listed above requires permission by the author.
"""
Reads a file provided by the user and print the value at each row

The file given by the user should be a text file containing one floating point number per line

"""

from ListAsArray import List #Use either ListAsTwoCell or ListAsArray

aList = List()

file_name = input("Name of file to be read: ")
floatFile = open(file_name, 'r') 

#Inserts value converted to float to last position in aList
pos = aList.end()
for line in floatFile:
    aList.insert(pos, float(line))
    pos = aList.end()
    
floatFile.close()



printformat= "Line {:<2d} in the file has the value {}"

#Prints values in the list from start to end position
#Inspired from Workshop 1 lösningsförslag övning 2 (printDLL(l))

pos = aList.first()
count = 1

while pos != aList.end():
    print(printformat.format(count, aList.inspect(pos)))
    pos = aList.next(pos)
    count += 1
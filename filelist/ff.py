# -*- coding: utf-8 -*- 

from os.path import isfile, join
from os import listdir

def searching(the_list, indent=False, level=0):
    print( "\n"+ the_list )

    items = listdir(the_list)
    items.sort()

    for each_item in items:
        if isfile(join(the_list, each_item)):
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
                print(each_item)
        else:
            searching(join(the_list, each_item), indent, level+1)



path_dir="/home/jmkim/_Security/00.Fuzz/2018_Signage_Fuzz/2018_Signage_Fuzz_Data_Media/fuzzdata"

mylist = listdir(path_dir) # ['bmp', 'rm', '3gp', 'mp4', 'jpg', 'png', 'avi', 'mkv']

mylist.sort() #정렬도 가능하다

for mypath in mylist:
    #print(join(path_dir, mypath))
    
    searching(join(path_dir, mypath), True, 1)
    #print(isfile(join(path_dir, myfile)), end=" ")
    #if isfile(join(path_dir, myfile)):
    #    print(myfile + " is FILE")
    #else:
    #    print(myfile + " is DIR")


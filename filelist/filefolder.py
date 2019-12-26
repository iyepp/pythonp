# -*- coding: utf-8 -*- 

from os.path import isfile, join
from os import listdir

path_dir="/home/jmkim/_Security/00.Fuzz/2018_Signage_Fuzz/2018_Signage_Fuzz_Data_Media/fuzzdata/avi"

file_list = listdir(path_dir)

file_list.sort() #정렬도 가능하다

for myfile in file_list:
    print(isfile(join(path_dir,myfile)), end=" ")
    if isfile(join(path_dir,myfile)):
        print(myfile + " is FILE")
    else:
        print(myfile + " is DIR")


# -*- coding: utf-8 -*- 

import os

path_dir="/home/jmkim/_Security/00.Fuzz/2018_Signage_Fuzz/2018_Signage_Fuzz_Data_Media/fuzzdata/avi"

file_list = os.listdir(path_dir)

file_list.sort() #정렬도 가능하다

for myfile in file_list:
    print(myfile)


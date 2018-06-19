import printColourGrid
import numpy
from os import listdir

directory_path = '.'
file_types = ['npy']

np_files = {dir_content: numpy.load(dir_content)
           for dir_content in listdir(directory_path)
           if dir_content.split('.')[-1] in file_types}

for file in np_files:
    mylist = numpy.load(file)
    printColourGrid.create_coloring(mylist, len(mylist), 10, name=file[:-4])
    
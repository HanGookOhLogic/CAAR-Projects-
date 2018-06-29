import printColorGrid
import numpy
from os import listdir

locations = ['SAT', 'SAT_iter', 'sim_annealing']
for location in locations:
    directory_path = './colorarrays/' + location + '/'
    file_types = ['npy']

    np_files = {dir_content: numpy.load(directory_path + dir_content)
                for dir_content in listdir(directory_path)
                if dir_content.split('.')[-1] in file_types}
    
    for file in np_files:
        filename = './Colorings/' + location + '/' + file[:-4]
        printColorGrid.create_coloring(np_files[file], len(np_files[file]), 10, name=filename)
        print 'Fig saved'
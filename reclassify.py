# This is used to reclassify the claasified datasets.
# Move images in different kinds of folders to a new one and add the folder name.
# For example: folder caltech256 has 256 different folders in it and each folder represent different kind of pictures
# use reclassify.py to create a new folder called database
# this folder can move all images in databseClassified folder and can create queryImgs.txt and databaseClasses.txt which
# are waiting for call.

import os
import fnmatch
import shutil
import random
import math

query_percentage = 0.5  #

dict = "static/img"  # set new path
databaseClass = 'databaseClassified'

if not os.path.exists(dict):
    os.makedirs(dict)

new_Path = os.path.abspath(dict)

# traverse the folder
f = open("./databaseClasses.txt", "w")
g = open("./queryImgs.txt", "w")
for r, d, fi in os.walk(databaseClass):
    for i, each_folder in enumerate(d):
        # get the dict path
        path = '/'.join([r, each_folder])
        file_num = len((os.listdir(path))) # number of subfiles

        #  create the query images
        index = random.sample(range(0,file_num), int(math.floor(query_percentage*file_num)))
        # list all the files using directory path
        for ind, str_each_file in enumerate(os.listdir(path)):
            # now add the new one
            new_name = '{0:03}'.format(i + 1) + '_' + each_folder + '_' + str_each_file
            if ind in index:
                g.writelines('%s\n' % new_name)
                # full path for both files
            str_old_name = '/'.join([path, str_each_file])
            str_new_name = '/'.join([new_Path, new_name])

            # now rename using the two above strings and the full path to the files
            shutil.copy2(str_old_name, str_new_name)

            #  we can print the folder name so we know that all files in the folder are done
        print '%s, %d images' % (each_folder, file_num)
        f.writelines('%s %d\n' % ('{0:03}'.format(i + 1) + '_' + each_folder, file_num))
g.close()
f.close()


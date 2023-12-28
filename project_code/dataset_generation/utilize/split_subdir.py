# _*_ encoding:utf-8 _*_
import os
import sys
from shutil import copyfile
 
 
origin_path = r'C:\FMServer\cfx-server-data-master\videos'       # the directory where the target files are located
 
filelist = os.listdir(origin_path)
 
for image_index in range(len(filelist)):
    if image_index <= 2000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '1-2000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)
        os.remove(src_fileName)

    elif image_index <= 4000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '2000-4000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)
        os.remove(src_fileName)

    elif image_index <= 6000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '4000-6000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)
        os.remove(src_fileName)

    elif image_index <= 8000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '6000-8000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)
        os.remove(src_fileName)

    elif image_index <= 10000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '8000-10000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)
        os.remove(src_fileName)

    elif image_index <= 12000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '10000-12000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)

        os.remove(src_fileName)

    elif image_index <= 14000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '12000-14000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)
        os.remove(src_fileName)

    elif image_index <= 16000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '14000-16000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)
        os.remove(src_fileName)

    elif image_index <= 18000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '16000-18000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)
        os.remove(src_fileName)

    elif image_index <= 20000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '18000-20000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)
        os.remove(src_fileName)

    elif image_index <= 22000 :
        fileName = filelist[image_index] # '1.png'
        fileClass = '20000-22000' # The first letter of the file name, including '1', '2', '3', '4', '5', '6', '7', '8', '9'
        filePath = origin_path + '\\' + fileClass + '\\' # The path to which the file should be assigned
        src_fileName = origin_path + '\\'+fileName
        tar_fileName = filePath + '\\'+fileName
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            print('create folder ', image_index)
        copyfile(src_fileName,tar_fileName)
        print('copyfile', image_index)
        os.remove(src_fileName)
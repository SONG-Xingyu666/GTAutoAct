input_file = open(r'D:\FXServer\cfx-server-data-master\resources\[scripts]\animation\client\animations.lua')    
input_file_lines = input_file.readlines()
output_file = open(r'D:\FXServer\cfx-server-data-master\resources\[scripts]\animation\client\animations_swim.lua','w')
index = 0
for line in input_file_lines:
    index += 1
    if 'div' in line:
        continue
    # info = line.split('\'')
    output_file.write(line)
    # if len(info) >3: 
    #     if float(info[5]) > 15:
    #         continue

    # if len(info) >3: 
    #     dict = info[1]
    #     anim = info[3]
    #     if 'drink' == anim:
    #         output_file.write(line)
    # if index % 2 ==0:
    #     continue



input_file.close()
output_file.close()
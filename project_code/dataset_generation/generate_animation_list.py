# generate_animation_list.py
# generate animation list 
input_file = open(r'C:\FMServer\cfx-server-data-master\animation_lists\animations_walk.txt')    
input_file_lines = input_file.readlines()
output_file = open(r'C:\FMServer\cfx-server-data-master\resources\[scripts]\animation\client\animations_walk.lua','w')
output_file.write('Animations = { \n')
for line in input_file_lines:
    info = line.split()
    info_str = str(info)[1:-1]

    output_file.write(str(info))
    output_file.write(',')
    output_file.write('\n')


output_file.write('}')
input_file.close()
output_file.close()

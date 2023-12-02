# Convert animation list txt file into lua

def txt2lua(input_path, output_path):
    input_file = open(input_path)    
    lines = input_file.readlines()
    output_file = open(output_path,'w')
    output_file.write('Animations = { \n')
    for line in lines:
        info = line.strip().split(' ')
        dict = info[0]
        anim = info[1]
        duration = info[2]
        string = '{'+"'"+dict+"'"+','+"'"+anim+"'"+','+"'"+duration+"'"+'}'+','+'\n'
        output_file.write(string)

    output_file.write('}')


if __name__ == '__main__':
    input_path = r'D:\FXServer\cfx-server-data-master\animation_lists\animations_swimming.txt'
    output_path = r'D:\FXServer\cfx-server-data-master\resources\[scripts]\animation\client\animations_swimming.lua'
    txt2lua(input_path, output_path)


    

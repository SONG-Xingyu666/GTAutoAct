# Filter animation with keywork

def filter_animation(input_path, output_path, keyword):
    input_file = open(input_path)    
    lines = input_file.readlines()
    output_file = open(output_path,'w')
    index_all = 0
    index_key = 0
    for line in lines:
        info = line.split(' ')
        dict = info[0]
        anim = info[1]
        duration = info[2]
        print('animation', index_all)
        index_all += 1
        if keyword in dict or keyword in anim:
            output_file.write(line)
            print('find', index_key)
            index_key += 1

    input_file.close()
    output_file.close()


if __name__ == '__main__':
    input_path = r'D:\FXServer\cfx-server-data-master\animation_lists\animations_duration_without0.txt'
    output_dir = r'D:\FXServer\cfx-server-data-master\animation_lists'
    keyword = 'swimming'
    output_path = output_dir + '\\' + 'animations_' + keyword + '.txt'
    filter_animation(input_path, output_path, keyword)
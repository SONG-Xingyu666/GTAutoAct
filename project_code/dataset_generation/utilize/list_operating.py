# list_operating.py
# delete the action with 0 duration
file = open('animations_duration_playable.txt')    
lines = file.readlines()
file_new = open('animations_duration_without0.txt','w')
for line in lines:
    animation = line.split()
    if animation[2] != '0':
        file_new.write(line)
file_new.close()

# Generate animation list
import os
onim_folder = r'demo\animations'
list_path = r'demo\animations_H36M.lua'
f = open(list_path,'w')
f.write('Animations = { \n')
files = os.listdir(onim_folder)
for file in files:
    if file.split('.')[-1] == 'ycd':
        dic = file.split('.ycd')[0]
        anim = dic.split('@')[-1]
        dura = float(anim.split('_')[-1]) / 30
        f.write('{')
        f.write('\'')
        f.write(dic)
        f.write('\', ')
        f.write('\'')
        f.write(anim)
        f.write('\', ')
        f.write('\'')
        f.write(str(dura))
        f.write('\'')
        f.write('},\n')
f.write('}')
f.close()
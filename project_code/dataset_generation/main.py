from utilize.auto_collection import change_screen_to_game, set_animation_mod, create_folder, recording_animation, next_animation

if __name__ == '__main__':
    #############################################################################
    # VARIABLE DECLARATIOIN
    #############################################################################

    output_dir = r'videos'

    # For in game animation information obtaining  
    
    animation_info_path = r'resources\[scripts]\animation\client\animations.lua'
    

    # For by list animation information obtaining
    keyword = 'H36M'
    postition_num = 3
    location_num = 4
    animation_num = 284

    #############################################################################
    # ANIMATION CONFIGURATION
    #############################################################################

    # change to game
    change_screen_to_game()


    # turn on animation mode
    set_animation_mod()
    
    # Create folder for animations of same keyword
    output_dir = create_folder(output_dir, keyword)

    #############################################################################
    # OBTAINING INFORMATION, PLAYING ANIMATION, RECORDING, TRIMMING, LABELING
    #############################################################################
    
    f = open(animation_info_path)
    anim_list = f.readlines()


    for i in range(1, animation_num):
        # Using all animations list, obtaining animation information in game    
        print(anim_list[i])

        # dict, anim, duration = obtain_animation_info_ingame(animation_info_path, keyword)
        dict = anim_list[i].split('\'')[1]
        anim = anim_list[i].split('\'')[3]
        duration = float(anim_list[i].split('\'')[5])
        animation_name = anim
        animation_dir = create_folder(output_dir, animation_name)
        recording_animation(animation_dir, dict, anim, duration, location_num, postition_num)
        next_animation()


    #############################################################################
    # FINISH
    #############################################################################
    

    # turn off animation mode
    set_animation_mod()





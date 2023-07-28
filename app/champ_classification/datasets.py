import cv2
import os


# Coordinate
ban_width = 0.023154
pick_width = 0.048811
ban_pic_distance = 0.031289     # 가로
pick_pic_distance = 0.112597    # 세로

coordinate = {'ban_champ' : [(0.010638, 0.041249), (0.041927, 0.041249), (0.073216, 0.041249), (0.104505, 0.041249), (0.135794, 0.041249), 
                           (0.841051, 0.041249), (0.87234, 0.041249), (0.903629, 0.041249), (0.934918, 0.041249), (0.966207, 0.041249)],
              'pick_ally_1' : (0.042553, 0.144928), 
              'pick_ally_2' : (0.042553, 0.257525), 
              'pick_ally_3' : (0.042553, 0.370122), 
              'pick_ally_4' : (0.042553, 0.482719), 
              'pick_ally_5' : (0.042553, 0.595316), 
              'pick_enemy_1' : (0.933667, 0.144928), 
              'pick_enemy_2' : (0.933667, 0.257525), 
              'pick_enemy_3' : (0.933667, 0.370122), 
              'pick_enemy_4' : (0.933667, 0.482719), 
              'pick_enemy_5' : (0.933667, 0.595316)
              }


def crop_trim(bg_img, trim_path, coord: tuple, save_name: str):
    bg_x = bg_img.shape[1]  # 가로 길이
    bg_y = bg_img.shape[0]  # 세로 길이
    a, b = coord

    x = round(bg_x * a)
    y = round(bg_y * b)
    if 'ban_champ' in save_name:
        w = round(bg_x * ban_width)
    else:
        w = round(bg_x * pick_width)
    h = w
    roi = bg_img[y:y+h, x:x+h]
    
    # img save
    cv2.imwrite(trim_path + 'trim_' + save_name + '.png', roi)


def makeData(img_data):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, "trim_result/")

    bg = img_data
    for key, _ in coordinate.items():
        if key=='ban_champ':
            for i in range(len(coordinate['ban_champ'])):
                crop_trim(bg, file_path, coordinate['ban_champ'][i], key+str(i))
        else:
            crop_trim(bg, file_path, coordinate[key], key)

    print('Saved Data')

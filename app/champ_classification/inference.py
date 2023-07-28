import argparse
import os
import torch
from torchvision import transforms
from PIL import Image
from datetime import datetime

current_dir = os.path.dirname(os.path.realpath(__file__))

# GPU 사용
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print ("device:[%s]."%(device))

# img transform value
trans = transforms.Compose([transforms.Resize((30, 30)),
                            transforms.ToTensor(), 
                            transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])

# class (champion name)
classes = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 
           'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'DrMundo', 'Draven', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 
           'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'KSante', 
           'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 
           'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'Milio', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Naafiri', 'Nami', 'Nasus', 
           'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'None', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 
           'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 
           'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 
           'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 
           'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']


def getName(img:str, model:str):
    img = Image.open(img).convert('RGB')
    
    if device=='cuda:0':
        champ_img = trans(img).float().to(device)
    else:
        champ_img = trans(img).float()

    # net = CNNmodel().to(device)
    # net.load_state_dict(torch.load(model))
    if device=='cuda:0':
        net = torch.load(model)
    else:
        net = torch.load(model, map_location=torch.device('cpu'))
    
    net.eval()
    outputs = net(champ_img)
    _, predicted = torch.max(outputs, 1)

    predict_champ = classes[predicted]

    return predict_champ


def getChampNameList():
    data_dir = os.path.join(current_dir, "trim_result/")
    model_dir = os.path.join(current_dir, "model/CNN_Champion.pt")

    # Data 불러오기
    data_list = os.listdir(data_dir)
    data_list.sort()

    # CNN 모델 불러오기
    model = model_dir

    # Result
    result = []

    # 모델 돌리기
    for img_name in data_list:
        aftermodel = getName(data_dir+img_name, model)
        if aftermodel=='None':
            aftermodel = None
            result.append(aftermodel)
        else:
            result.append(aftermodel)
    
    # 결과 저장
    print('Saved Results')

    return result
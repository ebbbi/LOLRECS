import torch

import yaml
import numpy as np


def get_config(config_path= "./app/assets/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

config = get_config()
name2id = config["name2id"]
id2name = config["id2name"]
idmap = config["idmap"]
ch_pos = config["champ_pos"]


def inference(alley, enemy, banlist, mastery, model_path = "./app/assets/"):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.jit.load(f"{model_path}/model_scripted.pt", map_location = device)
    model.eval()
    
    alley = [name2id[x] for x in alley if x]
    enemy = [name2id[x] for x in enemy if x]
    banlist = [name2id[x] for x in banlist if x]
    
    ax = np.zeros(4, dtype = int)
    ex = np.zeros(5, dtype = int)
    if alley: 
        ax[-len(alley):] = alley
    if enemy:
        ex[-len(enemy):] = enemy    
    
    input = torch.from_numpy(np.concatenate((ex, ax), axis=0)).long().unsqueeze(0).to(device)
    pos = torch.arange(9).unsqueeze(0).to(device)
        
    with torch.no_grad():
        preds = model(input, pos)
    
    preds = preds.to("cpu").detach().numpy()[0]  

    alpha = 1 if alley or enemy else 2 #control personalizaion  
    if mastery:      
        mastery = {idmap[int(k)] : v*alpha for k, v in mastery.items()}
        preds = np.array([x*mastery.get(i, 0.001) for i, x in enumerate(preds)]) 
    
    mask = alley+enemy+banlist
    preds[mask] = -np.inf
    
    items = np.argsort(preds)[::-1]
  
    results = [[], [], [], [], []]
    total_len = 0
    
    for x in items:
        if total_len==15:
            break
        for pos in ch_pos[x]:
            if len(results[pos])<3:
                results[pos].append(id2name[x])
                total_len+=1
                
    print(results)
    return results
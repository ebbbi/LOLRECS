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

def mastery_scaler(mastery, alpha):
    
    values = list(mastery.values())
    min_value = np.min(values)
    max_value = np.max(values)
    
    if min_value == max_value:
        return [0.5 * alpha]*len(values)
    else:
        v = [max(0.001, ((x - min_value)/(max_value - min_value))*0.5*alpha) for x in values]
        return v

def inference(alley, enemy, banlist, mastery, model_path = "./app/assets/"):
    alpha = 2  #control personalizaion - without picks       
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.jit.load(f"{model_path}/model_scripted_new.pt", map_location = device)
    model.eval()
    
    picks = [name2id[x] for x in alley+enemy if x]
    banlist = [name2id[x] for x in banlist if x]
    
    input = np.zeros(9, dtype = int)
    ban = np.zeros(10, dtype = int)
    
    if len(picks): 
        input[-len(picks):] = picks
        alpha = 1  #with picks 
    if len(banlist):
        ban[-len(banlist):] = banlist
    
    input = torch.from_numpy(input).long().unsqueeze(0).to(device)
    ban = torch.from_numpy(ban).long().unsqueeze(0).to(device)
    pos = torch.arange(9).unsqueeze(0).to(device)
        
    with torch.no_grad():
        preds = model(input, pos)
    
    preds = preds.to("cpu").detach().numpy()[0]  
      
    if mastery:        
        mastery = {idmap[k]:v for k, v in zip(mastery.keys(), mastery_scaler(mastery, alpha))}
        preds = np.array([x*mastery.get(i, 0.001) for i, x in enumerate(preds)]) 
    
    mask = picks+banlist
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

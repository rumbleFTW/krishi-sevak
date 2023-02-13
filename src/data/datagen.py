# %%
import random 
import pandas as pd
import json
import tqdm

# %%
base_data = open('./base_data.json')
base_dict = json.load(base_data)
base_dict

# %%
data = pd.DataFrame(columns=['soil', 'pH', 'type', 'temp', 'rainfall', 'humidity', 'sowing_month', 'crop'])
# %%
for i in tqdm.tqdm(range(0, 20_000)):
    key = random.choice(list(base_dict.keys()))
    row = [
            random.choice(base_dict[key]['soil']),
            random.uniform(base_dict[key]['pH'][0], base_dict[key]['pH'][1]),
            random.choice(base_dict[key]['type']),
            random.uniform(base_dict[key]['temp'][0], base_dict[key]['temp'][1]),
            random.uniform(base_dict[key]['rainfall'][0], base_dict[key]['rainfall'][1]),
            random.uniform(base_dict[key]['humidity'][0], base_dict[key]['humidity'][1]),
            random.choice(base_dict[key]['sowing_month']) - random.randint(1, 3) + 1,
            key
        ]
    data.loc[i] = row
# %%
data.info()
data.to_csv('./data.csv', index=None)
# %%

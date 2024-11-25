import yaml
import os

print("this script will set the amount of replicas of all the deployments to 2")

origs = []
for r, d, f in os.walk("."):
    for file in f:
        if 'deployment' in file and 'doubled' not in file:
            with open("."+os.sep+file,'r') as opened:
                origs.append(yaml.load(opened, Loader=yaml.FullLoader))
                
for orig in origs:
    orig["spec"]["replicas"]=2
    
for i, j in enumerate(origs):
    with open(str(j['spec']['template']['spec']['containers'][0]['name'])+'-deployment-doubled.yaml', 'w') as file:
        yaml.dump(j, file)
import yaml
yyy = None
# load original docker-compose
with open("../docker-compose.yml", "r") as f:
    yyy = yaml.load(f, Loader=yaml.FullLoader)
    for container_name, container_data in yyy["services"].items():
        # assign all containers to the default netowrk
        container_data["networks"]=["default"]
    try:
        # create the isolated networks and assign the dashboard-builder to it
        yyy["services"]["dashboard-builder"]["networks"]=["default","protected"]
        yyy["networks"]={"default":{"driver":"bridge"},"protected":{"driver":"bridge"}}
    except Exception as E:
        print("something failed:"+str(E))
        exit -1
    with open("docker-compose-with-networks.yml", "w") as f2:
        yaml.dump(yyy, f2)
xxx = None
# load the additional docker-compose
with open("docker-compose-iotappmaker.yml", "r") as f:
    xxx = yaml.load(f, Loader=yaml.FullLoader)
# merge them, the networks are already set up
for container_name, container_data in xxx[0]['services'].items():
    yyy[1]['services'][container_name]=container_data
# save the new compose
with open("docker-compose-final.yml", "w") as f3:
    yaml.dump(yyy, f3)
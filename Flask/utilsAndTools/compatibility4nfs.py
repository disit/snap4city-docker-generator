import yaml
import re
import os
import copy

#load the deployments into an array of yamls objects (nested dicts and lists)
print("Loading in original kubernetes yaml...")
thisdir = os.getcwd()+os.sep+'..'+os.sep+'kubernetes'
origs = []
for r, d, f in os.walk(thisdir):
    for file in f:
        if 'deployment' in file:
            with open(thisdir+os.sep+file,'r') as opened:
                origs.append(yaml.load(opened, Loader=yaml.FullLoader))

problematicNames = ['iotapp-','mongo-','orionbrokerfilter-']

#fix the security context for nfs reasons
print("Setting security context for all pods as 0,0,0")
for orig in origs:
    orig['spec']['template']['spec']['securityContext']={'runAsUser':0,'runAsGroup':0,'fsGroup':0}
    if orig['spec']['template']['spec']['containers'][0]['name']=='virtuoso-kb':
        orig['spec']['template']['spec']['containers'][0]['readynessProbe']={'exec':{'command':'["/bin/sh", "-c", "/root/servicemap/run.sh"]'},'initialDelaySeconds':25,'timeoutSeconds':30,'periodSeconds': 1000000000}
    elif orig['spec']['template']['spec']['containers'][0]['name']=='nifi':
        orig['spec']['template']['spec']['containers'][0]['readynessProbe']={'exec':{'command':'["/bin/sh", "-c", "./bin/nifi.sh set-single-user-credentials $#nifi-user#$ $#nifi-password#$"]'},'initialDelaySeconds':25,'timeoutSeconds':30,'periodSeconds': 1000000000}
    #elif orig['spec']['template']['spec']['containers'][0]['name']=='ldap-server':
    #    orig['spec']['template']['spec']['containers'][0]['initContainer']={'image':'disitlab/preconf-openldap:v3','command':'/bin/sh -c [ -z "$(ls -A /efsvolume/snap4volumes/ldap-conf)" ] && { echo "empty. do copy"; cp -R /etc/ldap/slapd.d/* /efsvolume/snap4volumes/ldap-conf; cp -R /var/lib/ldap/* /efsvolume/snap4volumes/ldap-db; true; } || { echo "not empty. no copy"; true;}'}
    #    orig['spec']['template']['spec']['containers'][0]['initContainer']['volumes'][0]=
print("Set the readyness probe for nifi to the setting of the credentials")
print("Set the readyness probe for virtuoso-kb to its startup script")
print("The readyness probes will be ran a few seconds after startup then each one billion seconds, or about 31 years")


# try to fix the names for the pvc
print("Merging all volumes, respectively in each container, into a single one")
lastkey = None
for orig in origs:
    if any(x in orig['spec']['template']['spec']['containers'][0]['name'] for x in problematicNames):
        continue
    try:
        cur = orig['spec']['template']['spec']['volumes']
        for i in range(len(cur)):
            if lastkey == cur[i]:
                lastkey = cur[i]
            else:
                temp = cur[i]
                cur.remove(temp)
                try:
                    # if there is a number at the end of the pvc, drop it
                    # it is caused by kompose making each volume indipendent from each other
                    temp['persistentVolumeClaim']['claimName']='claimnamereplaceme'
                    temp['name'] = temp['name'][:re.search(r"\d",temp['name']).end()-1]
                except AttributeError as E:
                    print('[Error] Did not fix because', E)

                cur.insert(i, temp)
    except KeyError as E:
        print('No volumes for the deployment',orig['spec']['template']['spec']['containers'][0]['name'])

# try to merge the volumes of a single deployment
for orig in origs:
    something = []
    #print(orig['spec']['template']['spec']['containers'][0]['name'])
    if any(x in orig['spec']['template']['spec']['containers'][0]['name'] for x in problematicNames):
        continue
    try:
        #for i in range(len(orig['spec']['template']['spec']['volumes'])):
        #    print(orig['spec']['template']['spec']['volumes'][i],'\n')
        # filter the duplicates
        orig['spec']['template']['spec']['volumes']=list({v['name']:v for v in orig['spec']['template']['spec']['volumes']}.values())
    except KeyError as E:
        print('No volumes for the deployment',orig['spec']['template']['spec']['containers'][0]['name'])

data = ''
print("Read the volumes from the docker-compose yaml")
with open(os.getcwd()+os.sep+'..'+os.sep+'docker-compose.yml','r') as getall:
    data=getall.read()

# get the volumes in the docker yaml
volumes = re.findall(" *- [\w/:.-]+:rw",data)
volumes = [volume.strip()[2:].split(':',1) for volume in volumes]

print("Converting the volumes mounts to be consistent with nfs requirements")
newlist = []
tempvolumes = copy.deepcopy(volumes)
for orig in origs:
    templist = []
    #print(orig['spec']['template']['spec']['containers'][0]['name'])
    try:
        for i in range(len(orig['spec']['template']['spec']['containers'][0]['volumeMounts'])):
            current = orig['spec']['template']['spec']['containers'][0]['volumeMounts'][i]
            try:
                number = current['name'][re.search(r'\d',current['name']).end()-1:]
                pos=re.search(r'\d',current['name']).end()-1
                addeddict = {'mountPath':current['mountPath'],'name':current['name'][:pos],'subPath':tempvolumes.pop(0)[0]}
                templist.append(addeddict)
                print(addeddict)
            except AttributeError as E:
                templist.append({'mountPath':current['mountPath'],'name':current['name'],'subPath':tempvolumes.pop(0)[0]})
                print('Did not fix')
            except IndexError as E:
                print('[Error] Something went wrong:',E)
    except KeyError as E:
        print('no volume in this deployment!')
    orig['spec']['template']['spec']['containers'][0]['volumeMounts']=templist
    newlist.append(templist)

#save the new files
for i, j in enumerate(origs):
    with open(str(j['spec']['template']['spec']['containers'][0]['name'])+'-deployment-new.yaml', 'w') as file:
        yaml.dump(j, file)
print("New yamls generated in this folder")
print("Done")

# Kubernetes implementation of Snap4City (experimental)
The Kubernetes implementation exports a Micro distribution to Kubernetes services and deployments. Given the differences on how volumes are handled, an additional folder is generated to store such volumes. This is still an experimental solution. Note that this guide won't go over the steps of setting up Kubernetes or a shared folder for each node of the Kubernetes cluster; see the appendices located at https://github.com/disit/snap4city-kubernetes in order to proceed.

# Premises

The Kubernetes distribution is built on top of a Micro distribution; all the files needed for the former also exist for the Kubernetes implementation. As such, you will find files for both.

# Presetup
The presetup-kuber.sh should set up the components for the first setup, including the setup.sh equivalent of the docker version of the distribution.

# Running
Using the console, go in the appropriate folder E.G. `cd path\to\snap4city`, where the usual configuration would be located. In doubt, `pwd` in the console where this file exists will tell you where the folder is located.
Most of the commands use can be found here: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
Run the command `kubectl apply -f .\kubernetes -n=$#k8-namespace#$`, which will run all the deployments and the services (some services won't exist because the deployment doesn't show a port) in the mentioned namespace.
To remove all resources of a give type in a given namespace, use `kubectl delete --all resources -n=$#k8-namespace#$`, where resources can be either `deployment` (the image running), `service` (exposing the aforementioned image), `pv` (persistent volume) and `pvc` (persistent volume claim). You can replace `-all` with the name of a specific resource should you wish to remove one object at a given time.
The error you might see refers to the docker-compose.yml file which doesn't obviously work with kubernetes, but is used to build all the other files. The error simply means that the file can't run, and produces no other effect whatsoever. Note that you won't get attached to any output of the pods.
In order to see the standard output of the running components, you need to use both logs and describe.
Example usage comes as `kubectl logs pod-in-question` and `kubectl describe pods pod-in-question`, but you aren't necessarily limited to pods.
The latter will output whatever the pod will output, while the latter can be used to determine why a component stopped by looking at the exit reasons. It will also provide other information.
To terminate a node, you can use `kubectl delete node node-in-question`.
Note that it will take some time for the changes to be applied, so you may need to wait a few seconds before continuing operations. Those are performed asychronously so the console won't just hang until it's done.
To run commands, such as opening a shell in a deployment, use `kubectl exec deployment/$#k8-namespace#$ -- some-command`.

# presetup-kuber.sh, setup.sh and post-setup.sh
Open presetup.sh and edit `replaceme` with the path of the shared folder for the pods, then run it.
`setup.sh` works just like the docker-compose distribution one.
The post-setup has *hopefully* been converted to work with Kubernetes.
The conditions for running them remain the same.

# Additional notes for eks installation
Go check out the the **kubernetes_eks** folder for additional instructions

Reference
https://blog.thoughtram.io/machine-learning/2016/09/23/beginning-ml-with-keras-and-tensorflow.html

Mounting on Amazon EC2:
https://hackernoon.com/keras-with-gpu-on-amazon-ec2-a-step-by-step-instruction-4f90364e49ac

## Build Docker Image

`cd` to Dockerfile `cd KerasDocker`

```
 docker build .
 docker login
```

Then some steps I forget to push it to the docker hub. Look it up and update this readme

## Networking to Tensorboard:

Start Docker on your machine

Run it, setting up port forwarding:

```
docker run -p 0.0.0.0:7007:6006 -it -v C:/users/skylar/documents/code/ml:/projects/ml --name keras-tf skywox/keras21tf14
```

## Note

Have to `rm` the docker each time before running again:

```
docker rm keras-tf
```

This will start in the bash of the VM so commands drop the `docker exec...` prefix

Execute:

```
python3 /projects/ml/tictactoe.py
```

Then run tensorboard:

```
tensorboard --logdir ./log --host 0.0.0.0 --port 6006
```

It will throw many `...Reloader tf_logging.py:86] Found more than one metagraph event per run...` messages and won't say that it's serving. However it will at the designated port

On Windows, `ipconfig` reveals `Ethernet adapter vEthernet (DockerNAT)` has ip of `10.0.75.1` which means we can connnect to tensorboard at `http://10.0.75.1:7007/` on the host machine

## Starting w/o networking

Using my image:

```
docker create -it -v C:/users/skylar/documents/code/ml:/projects/ml --name keras-tf skywox/keras21tf14
```

Then start it

```
docker start keras-tf
```

Execute

```
docker exec -it keras-tf python3 /projects/ml/keras_xor.py
```

To explore container:

```
docker exec -t -i keras-tf /bin/bash
```

Right now this generates many files and tensorboard doesn't like it
So I deleted all but one and ran tensorboard

```
docker exec -t -i keras-tf tensorboard --logdir ./log --host 0.0.0.0 --port 6006
```

and then installed and checked it with curl:

```
docker exec -t -i keras-tf apt-get update
docker exec -t -i keras-tf apt-get install curl
docker exec -t -i keras-tf curl http://localhost:6006/
```

which returns a bunch of HTML, which means it's working

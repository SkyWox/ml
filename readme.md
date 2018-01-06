## Build Docker Image

`cd` to Dockerfile `cd KerasDocker` note that this is a CPU-only version

```
 docker build .
 docker login
```

Then push to Docker hub.

## Starting Tensorboard with Networking:

Start Docker on your machine

Run it, setting up port forwarding:

```
docker run -p 0.0.0.0:7007:6006 -it -v C:/users/skylar/documents/code/ml:/projects/ml --name keras-tf skywox/keras21tf14
```

> ## Note
>
> Have to `rm` the docker each time before running again:
>
> ```
> docker rm keras-tf
> ```

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

On Windows, `ipconfig` reveals `Ethernet adapter vEthernet (DockerNAT)` has ip of `10.0.75.1` which means we can connnect to tensorboard at `http://10.0.75.1:7007/` on the host machine.
Note that internal port `6006` is forwarded to external port `7007`

## Running Jupyter Notebook

If needed, install jupyter

```
pip3 --no-cache-dir install jupyter
```

Then run jupyter with port forwarding for Docker

```
jupyter notebook --ip=0.0.0.0 --port=6006
```

## Futher Reading:

[Background](https://blog.thoughtram.io/machine-learning/2016/09/23/beginning-ml-with-keras-and-tensorflow.html)

[Mounting on Amazon EC2](https://hackernoon.com/keras-with-gpu-on-amazon-ec2-a-step-by-step-instruction-4f90364e49ac)

[Examples of Keras Dockerfiles](https://github.com/gw0/docker-keras)

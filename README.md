# surveillance-camera

## frame difference method

フレーム間差分法の実装(閾値は現在適当)

```bash
/home/shota/Projects/surveillance-camera/main.py
```
main.pyでリアルタイム画像を読み込んでいます．

```bash
/home/shota/Projects/surveillance-camera/config.yaml
```

## Environment

### Environment Create

```bash
conda env create -f=environment_nishiyama.yaml
```


### Environment Setting

We're using the virtual env  
```bash
source env/bin/activate
```
### python
python 3.8  

## Requirements
When the prototype is done,  
We will add the requirements.txt to the repository.  

## Docker

```bash
docker build .
docker run -it -v $(pwd):/workdir --env="DISPLAY=$DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --device /dev/video0:/dev/video0 [image id]```

## Docker Compose
```bash
docker-compose up --build -d
```

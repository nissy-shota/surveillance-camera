FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y && apt-get install -y tzdata && \
    apt-get install -y \
    python3.8 \
    python3-pip \
    libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workdir

RUN pip3 install --user --upgrade pip
COPY requirements.txt /workdir

RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]

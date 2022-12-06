FROM ros:noetic-ros-core as build-image

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  python3 -y \
  python3-pip -y \
  python-all-dev \
  libboost-python-dev \
  ffmpeg \
  vim \
  ros-noetic-cv-bridge \
  ros-noetic-pcl-ros

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip install boto3
RUN pip install opencv-python
RUN pip install uuid
RUN pip install requests-aws4auth
RUN pip install lxml
RUN pip install urllib3
RUN pip install bagpy
RUN pip install rospkg
RUN pip install progressbar

# Copy and install robologs Python module
ARG ROBOLOGS_SRC_DIR="/robologs"
RUN mkdir -p ${ROBOLOGS_SRC_DIR}
COPY ./python ${ROBOLOGS_SRC_DIR}
RUN pip install ${ROBOLOGS_SRC_DIR}

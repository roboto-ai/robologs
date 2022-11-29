# Define function directory
ARG FUNCTION_DIR="/function/"

FROM ros:noetic-ros-core as build-image

ENV DEBIAN_FRONTEND noninteractive

# Install aws-lambda-cpp build dependencies
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

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY ./ ${FUNCTION_DIR}

RUN pip install boto3
RUN pip install opencv-python
RUN pip install uuid
RUN pip install requests-aws4auth
RUN pip install lxml
RUN pip install urllib3
RUN pip install bagpy
RUN pip install rospkg
RUN pip install progressbar

ENV PYTHONPATH="$PYTHONPATH:/function"

# Include global arg in this stage of the build
ARG FUNCTION_DIR
ENTRYPOINT [ "/usr/bin/python3"]

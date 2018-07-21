# Udacity capstone project dockerfile
FROM ros:kinetic-robot
LABEL maintainer="olala7846@gmail.com"

# Install Dataspeed DBW https://goo.gl/KFSYi1 from binary
# adding Dataspeed server to apt
RUN sh -c 'echo "deb [ arch=amd64 ] http://packages.dataspeedinc.com/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-dataspeed-public.list'
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FF6D3CDA
RUN apt-get update

# setup rosdep
RUN sh -c 'echo "yaml http://packages.dataspeedinc.com/ros/ros-public-'$ROS_DISTRO'.yaml '$ROS_DISTRO'" > /etc/ros/rosdep/sources.list.d/30-dataspeed-public-'$ROS_DISTRO'.list'
RUN rosdep update
RUN apt-get install -y ros-$ROS_DISTRO-dbw-mkz
RUN apt-get upgrade -y
# end installing Dataspeed DBW

# install python packages
RUN apt-get install -y python-pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# install required ros dependencies
RUN apt-get install -y ros-$ROS_DISTRO-cv-bridge
RUN apt-get install -y ros-$ROS_DISTRO-pcl-ros
RUN apt-get install -y ros-$ROS_DISTRO-image-proc

# socket io
RUN apt-get install -y netbase

RUN apt-get install -y protobuf-compiler 
RUN apt-get install -y python-pil 
RUN apt-get install -y python-lxml 
RUN apt-get install -y python-tk

RUN pip install --user Cython
RUN pip install --user contextlib2
RUN pip install --user jupyter
RUN pip install --user matplotlib

RUN git clone https://github.com/tensorflow/models.git /usr/local/lib/python2.7/dist-packages/tensorflow/models
RUN git clone https://github.com/cocodataset/cocoapi.git /usr/local/lib/python2.7/dist-packages/tensorflow/cocoapi
RUN sh -c 'cd /usr/local/lib/python2.7/dist-packages/tensorflow/cocoapi/PythonAPI && make && cp -r /usr/local/lib/python2.7/dist-packages/tensorflow/cocoapi/PythonAPI/pycocotools /usr/local/lib/python2.7/dist-packages/tensorflow/models/research/'

RUN apt-get install -y unzip

RUN curl -OL https://github.com/google/protobuf/releases/download/v3.2.0/protoc-3.2.0-linux-x86_64.zip >>  /tmp/protoc-3.2.0-linux-x86_64.zip
RUN sh -c 'cd /tmp/; unzip protoc-3.2.0-linux-x86_64.zip -d protoc3; mv protoc3/bin/* /usr/local/bin/; mv protoc3/include/* /usr/local/include/'
RUN sh -c 'cd /usr/local/lib/python2.7/dist-packages/tensorflow/models/research/; protoc object_detection/protos/*.proto --python_out=.'


RUN mkdir /capstone
VOLUME ["/capstone"]
VOLUME ["/root/.ros/log/"]
WORKDIR /capstone/ros

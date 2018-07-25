Steps

ubuntu@ip-172-31-4-64:/data/capstone/code/CarND-Capstone$ docker build . -t capstone
ubuntu@ip-172-31-4-64:/data/capstone/code/CarND-Capstone$ docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/   --rm -it capstone


Get Data
Get data from https://s3-us-west-2.amazonaws.com/udacitysdccapstonepublic/dataset-sdcnd-capstone.zip
The .record files already created in AWS GPU instance by following "Creating TFRecord files" section.
TODO: add the steps and the scripts into the repo


Follow this step to install the environment in Docker. Already coded in Docker file. No more action required.
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md

Refer to this step to train the model in Google Cloud and download to local
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_pets.md

Setup a Google Cloud Project

* Create a new Google Cloud project name: udacitycapstonejunior
* Install Google Cloud SDK

   71  export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
   72  echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
   75  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
   77  apt-get update && apt-get install google-cloud-sdk
   78  apt-get install google-cloud-sdk-app-engine-python
   79  apt-get install google-cloud-sdk-app-engine-python-extras
   80  gcloud init

   TODO: add above script to docker except gcloud init ( need input your own account)

* Enable the ML Engine APIs
* Set up a Google Cloud Storage (GCS) bucket: udacitycapstonejuniorbucket

# export YOUR_GCS_BUCKET=udacitycapstonejuniorbucket


root@4d7d44e46c7d:/capstone/modeltrain# gsutil cp data/dataset-sdcnd-capstone/sim_data.record gs://${YOUR_GCS_BUCKET}/data/
root@4d7d44e46c7d:/capstone/modeltrain# gsutil cp data/label_map.pbtxt gs://${YOUR_GCS_BUCKET}/data/label_map.pbtxt


Downloading a COCO-pretrained Model for Transfer Learning
root@4d7d44e46c7d:/capstone/modeltrain/data# wget http://storage.googleapis.com/download.tensorflow.org/models/object_detection/faster_rcnn_resnet101_coco_11_06_2017.tar.gz
root@4d7d44e46c7d:/capstone/modeltrain/data# tar -xvf faster_rcnn_resnet101_coco_11_06_2017.tar.gz
root@4d7d44e46c7d:/capstone/modeltrain/data# gsutil cp faster_rcnn_resnet101_coco_11_06_2017/model.ckpt.* gs://${YOUR_GCS_BUCKET}/data/


Configuring the Object Detection Pipeline
root@4d7d44e46c7d:/capstone/modeltrain/data# gsutil cp config/faster_rcnn_resnet101_udacitycapstonejunior.config gs://${YOUR_GCS_BUCKET}/data/faster_rcnn_resnet101_udacitycapstonejunior.config


root@4d7d44e46c7d:/capstone/modeltrain/data# cd /usr/local/lib/python2.7/dist-packages/tensorflow/models/research/
root@4d7d44e46c7d:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research# bash object_detection/dataset_tools/create_pycocotools_package.sh /tmp/pycocotools

t@4d7d44e46c7d:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research# python setup.py sdist
root@4d7d44e46c7d:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research# cd slim/
root@4d7d44e46c7d:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research/slim# python setup.py sdist

root@4d7d44e46c7d:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research/slim# cd ..
root@4d7d44e46c7d:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research# ls dist/object_detection-0.1.tar.gz
dist/object_detection-0.1.tar.gz
root@4d7d44e46c7d:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research# ls slim/dist/slim-0.1.tar.gz
slim/dist/slim-0.1.tar.gz
root@4d7d44e46c7d:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research# ls /tmp/pycocotools/pycocotools-2.0.tar.gz
/tmp/pycocotools/pycocotools-2.0.tar.gz


# From tensorflow/models/research/

root@4d7d44e46c7d:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research# gcloud ml-engine jobs submit training `whoami`_object_detection_udacitycapstone_`date +%m_%d_%Y_%H_%M_%S` \
>      --runtime-version 1.8 \
>      --job-dir=gs://${YOUR_GCS_BUCKET}/model_dir \
>      --packages dist/object_detection-0.1.tar.gz,slim/dist/slim-0.1.tar.gz,/tmp/pycocotools/pycocotools-2.0.tar.gz \
>      --module-name object_detection.model_main \
>      --region us-central1 \
>      --config object_detection/samples/cloud/cloud.yml \
>      -- \
>      --model_dir=gs://${YOUR_GCS_BUCKET}/model_dir \
>      --pipeline_config_path=gs://${YOUR_GCS_BUCKET}/data/faster_rcnn_resnet101_udacitycapstonejunior.config

It will start ml-engine with 5 worker node and 3 parameter server GPU nodes. 

Kill the job after a while, here we kill it in 2 hours

root@4d7d44e46c7d:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research# gcloud ml-engine jobs cancel root_object_detection_udacitycapstone_07_23_2018_01_44_48


Export Model from Google Cloud to Local:
root@56d3f826d30b:/capstone/ros# export YOUR_GCS_BUCKET=udacitycapstonejuniorbucket
root@56d3f826d30b:/capstone/ros# export CHECKPOINT_NUMBER=28564
root@56d3f826d30b:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research# gsutil cp gs://${YOUR_GCS_BUCKET}/model_dir/model.ckpt-${CHECKPOINT_NUMBER}.* /capstone/modeltrain/modeloutput/
root@56d3f826d30b:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research# python object_detection/export_inference_graph.py     --input_type image_tensor     --pipeline_config_path /capstone/modeltrain/data/config/faster_rcnn_resnet101_udacitycapstonejunior.config     --trained_checkpoint_prefix /capstone/modeltrain/modeloutput/model.ckpt-${CHECKPOINT_NUMBER}     --output_directory /capstone/modeltrain/modeloutput/exported_graphs


Copy object_detection_tutorial_udacityjunior.ipynb to /usr/local/lib/python2.7/dist-packages/tensorflow/models/research/object_detection/

Open Jupyter
root@56d3f826d30b:/usr/local/lib/python2.7/dist-packages/tensorflow/models/research/object_detection# /usr/bin/env python /root/.local/bin/jupyter-notebook --allow-root --ip 0.0.0.0 --no-browser ./object_detection_tutorial_udacityjunior.ipynb

Get the ip inside the docker with command #ip address

Run the code inside the ipython notebook. It will produce the predicted result.



###############################


Notes:
The raw data and trained models are too large, it was put into aws s3 folder. To get those data, run get_data.sh
The tensorflow models repo changes very frequent, here is the copy of the cod we use for this test. https://s3-us-west-2.amazonaws.com/udacitysdccapstonepublic/models.zip

#!/bin/bash

#Original Data & .record data
wget https://s3-us-west-2.amazonaws.com/udacitysdccapstonepublic/dataset-sdcnd-capstone.zip -P ./data/
unzip ./data/dataset-sdcnd-capstone.zip -d ./data/dataset-sdcnd-capstone

#Trained Model
mkdir modeloutput
wget https://s3-us-west-2.amazonaws.com/udacitysdccapstonepublic/exported_graphs.zip -P ./modeloutput/
unzip ./modeloutput/exported_graphs.zip -d ./modeloutput/

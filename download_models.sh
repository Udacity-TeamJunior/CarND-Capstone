#!/bin/bash

#Trained Model 
wget  https://s3-us-west-2.amazonaws.com/udacitysdccapstonepublic/light_classification/model_frozen_real/frcnn/frozen_inference_graph.pb -P ./ros/src/tl_detector/light_classification/model_frozen_real/frcnn/
wget  https://s3-us-west-2.amazonaws.com/udacitysdccapstonepublic/light_classification/model_frozen_sim/frcnn/frozen_inference_graph.pb -P ./ros/src/tl_detector/light_classification/model_frozen_sim/frcnn/

from styx_msgs.msg import TrafficLight
import tensorflow as tf
import numpy as np
import os
import cv2
import rospy
import yaml

MAX_IMAGE_WIDTH = 300
MAX_IMAGE_HEIGHT = 225

#model_type='frcnn'
model_type='ssd'

class TLClassifier(object):

    def __init__(self):
        #TODO load classifier
        config_string = rospy.get_param("/traffic_light_config")
        self.config = yaml.load(config_string)
        rospy.loginfo(self.config['detect_model']+model_type+'/frozen_inference_graph.pb')
        self.model_graph = self.import_graph(self.config['detect_model']+model_type+'/frozen_inference_graph.pb')
        self.session = tf.Session(graph=self.model_graph)

        self.classes = {1: TrafficLight.GREEN,
                        2: TrafficLight.RED,
                        3: TrafficLight.YELLOW, 
                        4: TrafficLight.UNKNOWN}


    def process_image(self, image):
        image = cv2.resize(image, (MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
        
    def run_inference_for_single_image(self, image_np, min_score_thresh=0.5):
        image_tensor = self.model_graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = self.model_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = self.model_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = self.model_graph.get_tensor_by_name('detection_classes:0')
        image_np = self.process_image(image_np)

        (boxes, scores, classes) = self.session.run(
            [detection_boxes, detection_scores, detection_classes],
            feed_dict={image_tensor: np.expand_dims(image_np, axis=0)})

        scores = np.squeeze(scores)
        classes = np.squeeze(classes)
        boxes = np.squeeze(boxes)

        for i, box in enumerate(boxes):
            if scores[i] > min_score_thresh:
                light_class = self.classes[classes[i]]
        #        rospy.loginfo("Traffic Light Class detected: %d", light_class)
                return light_class, scores[i]

        return None, None


    def import_graph(self,model_path):
        detection_graph = tf.Graph()

        with detection_graph.as_default():
          od_graph_def = tf.GraphDef()

          with tf.gfile.GFile(model_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        return detection_graph

    def get_classification(self, image):
        """Determines the color of the traffic light in the image
        Args:
            image (cv::Mat): image containing the traffic light
        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)
        """
        class_index, probability = self.run_inference_for_single_image(image)

        if class_index is not None:
            rospy.loginfo("class: %d, probability: %f", class_index, probability)

        return class_index

from styx_msgs.msg import TrafficLight
import tensorflow as tf
import numpy as np
import os
import cv2
import rospy
import yaml

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        self.model_graph = self.import_graph('light_classification/model_frozen_sim/frozen_inference_graph.pb')
        self.session = tf.Session(graph=self.model_graph)
        self.image_counter = 0
        self.classes = {1: TrafficLight.RED,
                        2: TrafficLight.YELLOW,
                        3: TrafficLight.GREEN,
                        4: TrafficLight.UNKNOWN}

        config_string = rospy.get_param("/traffic_light_config")
        self.config = yaml.load(config_string)


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
                self.save_image(image_np, light_class)
                rospy.logdebug("Traffic Light Class detected: %d", light_class)
                return light_class, scores[i]
            else:
                self.save_image(image_np, TrafficLight.UNKNOWN)

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
        #TODO implement light color prediction
        
        class_index, probability = self.run_inference_for_single_image(image)

        if class_index is not None:
            rospy.logdebug("class: %d, probability: %f", class_index, probability)

        return class_index

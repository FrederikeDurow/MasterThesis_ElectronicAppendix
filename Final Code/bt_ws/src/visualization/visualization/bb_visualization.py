import cv2
import rclpy
import logging
import py_trees
from rclpy.node import Node
from cv_bridge import CvBridge
from py_trees.common import Status
from sensor_msgs.msg import Image
from std_msgs.msg import String
# from custom_msgs.msg import StringArray 
from depthai_ros_msgs.msg import SpatialDetectionArray

########### ADD CLEAR LABEL LIST SERVICE


class BB_Forwarder(Node):

    def __init__(self):
        super().__init__('Object_Detection_Visualizer')
        self.all_labels = []
        # self.imageQueue = []
        self.resultsQueue = []
        self.bboxQueue = []
        self.bridge = CvBridge()

        # self.imageSubscriber = self.create_subscription(Image, '/color/image', self.image_callback, 10)
        self.detectionSubscriber = self.create_subscription(SpatialDetectionArray, '/color/yolov4_Spatial_detections', self.detection_callback, 10) #yolov4_detections

        # self.imgPublisher = self.create_publisher(Image, 'object_bounding_boxes', 10)
        self.labelPublisher = self.create_publisher(String, 'object_labels', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.callback)
        self.known_objects = ["person",        "bicycle",      "car",           "motorbike",     "aeroplane",   "bus",         "train",       "truck",        "boat",
        "traffic light", "fire hydrant", "stop sign",     "parking meter", "bench",       "bird",        "cat",         "dog",          "horse",
        "sheep",         "cow",          "elephant",      "bear",          "zebra",       "giraffe",     "backpack",    "umbrella",     "handbag",
        "tie",           "suitcase",     "frisbee",       "skis",          "snowboard",   "sports ball", "kite",        "baseball bat", "baseball glove",
        "skateboard",    "surfboard",    "tennis racket", "bottle",        "wine glass",  "cup",         "fork",        "knife",        "spoon",
        "bowl",          "banana",       "apple",         "sandwich",      "orange",      "broccoli",    "carrot",      "hot dog",      "pizza",
        "donut",         "cake",         "chair",         "sofa",          "pottedplant", "bed",         "diningtable", "toilet",       "tvmonitor",
        "laptop",        "mouse",        "remote",        "keyboard",      "cell phone",  "microwave",   "oven",        "toaster",      "sink",
        "refrigerator",  "book",         "clock",         "vase",          "scissors",    "teddy bear",  "hair drier",  "toothbrush"]


        
    def image_callback(self, msg: Image) -> None:
        if msg:
            image=self.bridge.imgmsg_to_cv2(msg)
            self.imageQueue.append(image)
    
    def detection_callback(self, dai_msg: SpatialDetectionArray) -> None:
        try:
            if dai_msg:
                all_bboxes = [dai_msg.detections[i].bbox for i in range(len(dai_msg.detections))]
                self.bboxQueue.append(all_bboxes)
                all_results = [dai_msg.detections[i].results for i in range(len(dai_msg.detections))]
                self.resultsQueue.append(all_results)
        except Exception as e: 
            print(str(e))

    def callback(self):
        try: 
            # if self.imageQueue:
            #     image = self.imageQueue[-1]
            #     self.imageQueue.pop(0)

                if self.bboxQueue:
                    for i in range(len(self.bboxQueue[-1])):
                        bb = self.bboxQueue[-1][i]
                        center_x = bb.center.position.x
                        center_y = bb.center.position.y
                        size_x = bb.size_x
                        size_y = bb.size_y 

                        label = self.known_objects[int(self.resultsQueue[-1][i][0].class_id)]
                        self.all_labels.append(label)
                        label_msg = String()
                        label_msg.data = label
                        self.labelPublisher.publish(label_msg)
                        # cv2.rectangle(img=image, pt1=(int(center_x-0.5*size_x),int(center_y-0.5*size_y)), pt2=(int(center_x+0.5*size_x),int(center_y+0.5*size_y)), color=(255,0,0), thickness=2)
                        # cv2.putText(image, label, (int(center_x+0.5*size_x),int(center_y+0.5*size_y)),color=(0,0,255),fontFace=1, fontScale=1)

                    self.bboxQueue.clear()
                    self.resultsQueue.clear()
                # self.imgPublisher.publish(self.bridge.cv2_to_imgmsg(image,encoding="bgr8"))
                # label_msg = StringArray()
                # label_msg.data = self.all_labels
                
        except Exception as e: 
            print(str(e))
       

def main(args=None):
    rclpy.init(args=args)
    bt_sub = BB_Forwarder()
    rclpy.spin(bt_sub)
    bt_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
import math
import angles
import logging
import py_trees
import numpy as np
import tf_transformations as T
from py_trees.common import Status
from std_msgs.msg import Int32, Bool
from geometry_msgs.msg import PoseStamped
from audio_common_msgs.msg import AudioData
from behavior_tree.config.audio import RespeakerAudio
from rclpy.qos import QoSProfile, QoSDurabilityPolicy
from behavior_tree.config.interface import RespeakerInterface
from behavior_tree.config.settings import RESPEAKER_PARAMETERS



class Microphone(py_trees.behaviour.Behaviour):
    def __init__(self,name: str, logger: logging.Logger):
        super().__init__(name=name)
        self.logger = logger
        self.sensor_frame_id = 'respeaker_base'                  #self.declare_parameter('sensor_frame_id', 'respeaker_base')
        self.speech_prefetch = 0.5                  #self.declare_parameter('speech_prefetch', 0.5)
        self.update_period_s = 0.1                   #self.declare_parameter('update_period_s', 0.1)
        self.main_channel = 0                      #self.declare_parameter('main_channel', 0)
        self.speech_continuation = 0.5               #self.declare_parameter('speech_continuation', 0.5)
        self.speech_max_duration = 30.0               #self.declare_parameter('speech_max_duration', 7.0)
        self.speech_min_duration = 0.1               #self.declare_parameter('speech_min_duration', 0.1)
        self.doa_xy_offset = 0.0                     #self.declare_parameter('doa_xy_offset', 0.0)
        self.doa_yaw_offset = 90.0                    #self.declare_parameter('doa_yaw_offset', 90.0)

    def setup(self, **kwargs) -> None:
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = "Didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  # 'direct cause' traceability
        
        try: 
            self.respeaker = RespeakerInterface()
            if self.respeaker.read('CNIONOFF') != 0:
                for name_, value_ in RESPEAKER_PARAMETERS.items():
                    self.respeaker.write(name=name_,value=value_)

            self.respeaker_audio = RespeakerAudio(self.on_audio, suppress_error=True)
            self.colors = {"RED":0xFF0000,
                       "YELLOW":0xFFFF00,
                       "GREEN":0x00FF00,
                       "BLUE":0x0000FF}         
            self.current_color = "YELLOW"
            self.respeaker.pixel_ring.mono(self.colors[self.current_color])
            self.speech_audio_buffer = []
            self.is_speaking = False
            self.prev_is_voice = None
            self.prev_doa = None
            latching_qos = QoSProfile(depth=1,
                durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)
            self._pub_vad = self.node.create_publisher(Bool, 'vad', latching_qos)
            self._pub_doa_raw = self.node.create_publisher(Int32, 'doa_raw', latching_qos)
            self._pub_doa = self.node.create_publisher(PoseStamped, 'doa', latching_qos)
            self._pub_audio = self.node.create_publisher(AudioData, 'audio', 10)
            self._pub_audio_channel0 = self.node.create_publisher(AudioData, 'audio/channel0', 10)
            self.speech_prefetch_bytes = int(
                self.speech_prefetch * self.respeaker_audio.rate * self.respeaker_audio.bitdepth / 8.0)
            self.speech_prefetch_buffer = np.zeros(self.speech_prefetch_bytes, dtype=np.uint8)
            self.respeaker_audio.start()
    
            self.timer_led = None
            
        except Exception as e:
            self.logger.error(e)


    def on_audio(self, data, channel):
        if channel == self.main_channel:
            as_uint8 = data.astype(np.int16).tobytes()
            self._pub_audio_channel0.publish(AudioData(data=as_uint8))       

    def initialise(self) -> None:
        pass

    def update(self) -> Status:
        try:
            color = py_trees.blackboard.Blackboard.get("LED_COLOR")
            if color != self.current_color:
                self.current_color = color
                self.respeaker.pixel_ring.mono(self.colors[self.current_color])
        
            is_voice = self.respeaker.is_voice()
            doa_rad = math.radians(self.respeaker.direction - 180.0)
            doa_rad = angles.shortest_angular_distance(
                doa_rad, math.radians(self.doa_yaw_offset))
            doa = math.degrees(doa_rad)

            # vad
            if is_voice != self.prev_is_voice:
                self._pub_vad.publish(Bool(data=is_voice == 1))
                self.prev_is_voice = is_voice

            # doa
            if doa != self.prev_doa:
                self._pub_doa_raw.publish(Int32(data=int(doa)))
                self.prev_doa = doa

            msg = PoseStamped()
            msg.header.frame_id = self.sensor_frame_id
            ori = T.quaternion_from_euler(math.radians(doa), 0, 0)
            msg.pose.position.x = self.doa_xy_offset * np.cos(doa_rad)
            msg.pose.position.y = self.doa_xy_offset * np.sin(doa_rad)
            msg.pose.orientation.w = ori[0]
            msg.pose.orientation.x = ori[1]
            msg.pose.orientation.y = ori[2]
            msg.pose.orientation.z = ori[3]
            self._pub_doa.publish(msg)
            return py_trees.common.Status.SUCCESS 
        except Exception as e:
            self.logger.error(str(e))
        return py_trees.common.Status.FAILURE
    

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
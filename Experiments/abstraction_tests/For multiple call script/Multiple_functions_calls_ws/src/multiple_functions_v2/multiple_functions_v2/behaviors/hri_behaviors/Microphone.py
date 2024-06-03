#!/usr/bin/env python3
import py_trees
import numpy as np
from py_trees.common import Status
from custom_msgs.msg import Audio 
import usb.core
import usb.util

import rclpy
import logging
import rclpy.time
import rclpy.duration
import rclpy.timer
import math
import numpy as np
import angles
import tf_transformations as T
from py_trees.common import Status
from rclpy.qos import QoSProfile, QoSDurabilityPolicy
from audio_common_msgs.msg import AudioData
from std_msgs.msg import Int32, Bool, ColorRGBA
from geometry_msgs.msg import PoseStamped
from behavior_tree.config.audio import RespeakerAudio
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

            self.speech_audio_buffer = []
            self.is_speaking = False
            #self.speech_stopped = self.get_clock().now()
            self.prev_is_voice = None
            self.prev_doa = None
            latching_qos = QoSProfile(depth=1,
                durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)
            self._pub_vad = self.node.create_publisher(Bool, 'vad', latching_qos)
            self._pub_doa_raw = self.node.create_publisher(Int32, 'doa_raw', latching_qos)
            self._pub_doa = self.node.create_publisher(PoseStamped, 'doa', latching_qos)
            self._pub_audio = self.node.create_publisher(AudioData, 'audio', 10)
            self._pub_audio_channels = {c: self.node.create_publisher(AudioData, 'audio/channel%d' % c, 10) for c in self.respeaker_audio.channels}
            #self._pub_speech_audio = self.create_publisher(AudioData, 'speech_audio', 10)
            #self._timer = self.node.create_timer(self.update_period_s, self.on_timer)

            self.speech_prefetch_bytes = int(
                self.speech_prefetch * self.respeaker_audio.rate * self.respeaker_audio.bitdepth / 8.0)
            self.speech_prefetch_buffer = np.zeros(self.speech_prefetch_bytes, dtype=np.uint8)
            self.respeaker_audio.start()
    
            self.timer_led = None
            self.sub_led = self.node.create_subscription(ColorRGBA, "status_led", self.on_status_led, 1)
            
        except Exception as e:
            self.logger.error(e)


    def on_audio(self, data, channel):
        as_uint8 = data.astype(np.int16)
        as_uint8 = as_uint8.tobytes()
    
        channel_pub = self._pub_audio_channels[channel]
        if channel_pub.get_subscription_count() > 0:
            channel_pub.publish(AudioData(data=as_uint8))
        if channel == self.main_channel:
            if self._pub_audio.get_subscription_count() > 0:
                self._pub_audio.publish(AudioData(data=as_uint8))
            #if self.is_speaking:
            #    if len(self.speech_audio_buffer) == 0:
            #        self.speech_audio_buffer = [self.speech_prefetch_buffer]
            #    self.speech_audio_buffer.append(as_uint8)
            #else:
            #    self.speech_prefetch_buffer = np.roll(self.speech_prefetch_buffer, -len(as_uint8))
            #    self.speech_prefetch_buffer[-len(as_uint8):] = as_uint8

    # def on_timer(self):
    #     #stamp = self.get_clock().now()
        
                    
    def on_status_led(self, msg):
        self.respeaker.set_led_color(r=msg.r, g=msg.g, b=msg.b, a=msg.a)
        if self.timer_led and self.timer_led.is_alive():
            self.timer_led.destroy()
        self.timer_led = rclpy.timer.Timer(rclpy.duration.Duration(1.0),
                                     lambda e: self.respeaker.set_led_trace(),
                                     oneshot=True)
        
    def initialise(self) -> None:
        pass

    def update(self) -> Status:
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
        #msg.header.stamp = stamp.to_msg()
        ori = T.quaternion_from_euler(math.radians(doa), 0, 0)
        msg.pose.position.x = self.doa_xy_offset * np.cos(doa_rad)
        msg.pose.position.y = self.doa_xy_offset * np.sin(doa_rad)
        msg.pose.orientation.w = ori[0]
        msg.pose.orientation.x = ori[1]
        msg.pose.orientation.y = ori[2]
        msg.pose.orientation.z = ori[3]
        self._pub_doa.publish(msg)
        return py_trees.common.Status.SUCCESS 

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
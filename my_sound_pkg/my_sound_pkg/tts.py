import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from action_msgs.msg import GoalStatus

from custom_action_interfaces.action import Tts
from rclpy.callback_groups import ReentrantCallbackGroup
import pyaudio
import threading
import numpy as np
from TTS.api import TTS
import sounddevice as sd


from std_msgs.msg import String
import time
# Initialize TTS with the target model name
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC_ph", progress_bar=True)




class Speaker(Node):
    def say(self,text):
        self.get_logger().info(f'saying {text}')
        data = tts.tts(text)
        sd.play(data, samplerate=22050)
        status = sd.wait()

    def __init__(self):
        
        super().__init__('Tts_action_server')
        self.get_logger().info('Starting....')
        self.current_goal_handle = None
        self._goal_queue_lock = threading.Lock()
        self._sound_device_lock = threading.Lock()
        self.callback_group = ReentrantCallbackGroup()
        self.queue=[]
        self._action_server = ActionServer(
            self,
            Tts,
            'Tts',
            handle_accepted_callback=self.handle_accepted_callback,
            execute_callback=self.execute_callback,
            callback_group=self.callback_group)

    def  execute_callback(self, goal_handle):
        self.get_logger().info(f'Executing goal... with senteces={goal_handle.request.sentences}')
        higer_priority_found = False
        sentences=goal_handle.request.sentences

        for sentence in sentences:
            if GoalStatus.STATUS_EXECUTING==goal_handle.status:
                # for item in self.queue:
                #     self.get_logger().info(f"Inside for loop")
                #     if item.request.order > goal_handle.request.order:
                #         higer_priority_found=True
                #         break
                # if higer_priority_found:
                #     self.get_logger().info(f'has a higher priority task in the queue')
                #     break
                if sentence:
                    with self._sound_device_lock:
                        self.say(sentence)
        self.current_goal_handle.succeed()
        result = Tts.Result()
        if self.queue:
            with self._goal_queue_lock:            
                self.current_goal_handle=self.queue.pop()
                self.get_logger().info(f'accpted a new goal{self.current_goal_handle.status}')
                self.current_goal_handle.execute()
        else:    
            self.current_goal_handle=None
        return result
    
    def handle_accepted_callback(self, goal_handle):
        self.get_logger().info(f'accpted a new goal{goal_handle.request.sentences} it has status= {goal_handle.status}')
        priority=goal_handle.request.order

        with self._goal_queue_lock:
            if self.current_goal_handle:
                self.get_logger().info(f"something already executing")
                #sd.stop()
                if priority<self.current_goal_handle.request.order:
                    self.queue.append(goal_handle)
                    # try:
                    #     say("something already executing")
                    # except:
                    #     self.get_logger().info(f"raised an exception")
                    self.get_logger().info(f"{dir(self.current_goal_handle)}")
                elif  GoalStatus.STATUS_EXECUTING==self.current_goal_handle.status: 
                    # self.current_goal_handle.abort()
                        
                    self.current_goal_handle.abort()
                    self.get_logger().info(f'cancelling the {self.current_goal_handle.request.order} and starting {goal_handle.request.order}')
                    goal_handle.execute()
                    self.current_goal_handle=goal_handle
                else:
                    goal_handle.execute()
                    self.current_goal_handle=goal_handle
            else:
                goal_handle.execute()
                self.current_goal_handle=goal_handle

            #self.current_goal_handle.abort()
        
            
            
        
        #goal_handle.execute()
        


def main(args=None):
    rclpy.init(args=args)
    Tts_action_server = Speaker()
    executor = MultiThreadedExecutor()
    rclpy.spin(Tts_action_server, executor=executor)


if __name__ == '__main__':
    main()

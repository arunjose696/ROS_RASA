# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import rclpy
from typing import Any, Text, Dict, List
import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.events import ReminderScheduled, ReminderCancelled
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

rclpy.init(
    
)


from action_msgs.msg import GoalStatus
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from custom_action_interfaces.action import Tts
class TTS_client(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Tts, 'Tts')

    def send_goal(self, order,sentences):
        goal_msg = Tts.Goal()
        goal_msg.order = order
        goal_msg.sentences = sentences

        self._action_client.wait_for_server()

        return self._action_client.send_goal_async(goal_msg)
action_client = TTS_client()

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("inside action action")
        bot_messages=""" I just heard you greeting me. Not many people greet robots. That is why we are not so social."""
        sentences=bot_messages.split('.')
        print(sentences)
        future = action_client.send_goal(10,sentences)
        dispatcher.utter_message(text=bot_messages)

        return []


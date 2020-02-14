from Message import *

from StpSwitch import *





class Switch(StpSwitch):




    def __init__(self, idNum, topolink, neighbors):

        super(Switch, self).__init__(idNum, topolink, neighbors)

        self.root = self.switchID

        self.distance = 0

        self.switch_through = self.switchID

        # Records if a switch needs to go through me to reach the root.

        self.through_me = {}




    def send_initial_messages(self):

        for destination in self.links:

            self.send_message(

                Message(self.root, self.distance, self.switchID, destination, False))

        return




    def process_message(self, message):

        self.through_me[message.origin] = message.pathThrough

        if (

            (message.root < self.root) or

            (message.root == self.root and message.distance + 1 < self.distance) or

            (message.root == self.root and message.distance + 1 ==

             self.distance and message.origin < self.switch_through)

        ):

            self.root = message.root

            self.distance = message.distance + 1

            self.switch_through = message.origin

            for destination in self.links:

                self.send_message(Message(self.root, self.distance,

                                          self.switchID, destination, destination == self.switch_through))

        return




    def generate_logstring(self):

        answers = filter(

            lambda link: self.through_me[link] or link == self.switch_through, self.links)

        return ', '.join(["{} - {}".format(self.switchID, neighbor) for neighbor in sorted(answers)])

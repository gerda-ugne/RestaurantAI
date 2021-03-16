import json

from aima3.search import Problem, Node
from flask import jsonify

class ClosestRestaurant(Problem):

    def actions(self, state):
        """Return actions in the current restaurant to:
        - scan the nearby area
        - travel to another restaurant """
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        After scanning: return locations available to travel to
        After travelling: return new coordinates for the agent
        """

        if (action == "travel"):
            return
        elif (action == "scan"):
            return

        raise NotImplementedError


class RestaurantNode(Node):
    """Data types:
        - Location is a list containing latitude and longitude"""

    def __init__(self, state, id, location, parent=None, action=None, path_cost=0):
        super(RestaurantNode, self).__init__()
        self.id = id
        self.location = location


class Solution:
    if __name__ == '__main__':

        restaurant_list = list()
        dataFile = open('dataset/file1.json')

        data = json.load(dataFile)
        dataFile.close()

        print(json.dumps(data, indent=4, sort_keys=False))


        """ Store the restaurant locations in the following format:
        "Name"  : "Location[x,y] by using dictionaries """
        restaurant_locations = dict()

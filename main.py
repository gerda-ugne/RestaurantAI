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

    def __init__(self, state, name, id, location, parent=None, action=None, path_cost=0):
        super(RestaurantNode, self).__init__(state, parent, action, path_cost)
        self.name = name
        self.id = id
        self.location = location

    def print(self):
        print("Name: " + self.name)
        print("States: " + self.state)
        print("ID: " + str(self.id))
        print("Location:" + self.location[0] + ", " +  self.location[1])
        print()

class Solution:
    if __name__ == '__main__':

        dataFile = open('dataset/file1.json')

        data = json.load(dataFile)
        dataFile.close()

        filteredData = dict()
        nRestaurants = data[0]['results_found']

        counter = 0
        restaurant_list = []
        for i in data[0]['restaurants']:
            print(i)
            restaurant_list.append(RestaurantNode(i['restaurant']['cuisines'],
                                                  i['restaurant']['name'],
                                                  i['restaurant']['R']['res_id'],
                                                  [i['restaurant']['location']['latitude'],
                                                   i['restaurant']['location']['longitude']]
                                                  ))
            counter += 1

        print(nRestaurants)
        print(counter)

        for restaurant in restaurant_list:
            restaurant.print()

        # print(json.dumps(data, indent=4, sort_keys=False))


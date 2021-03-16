import json
from abc import ABC

from aima3.search import Problem, Node, SimpleProblemSolvingAgentProgram
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
        available_actions = []
        if action == "travel":
            return
        elif action == "scan":
            return

        return available_actions

    def value(self, state):
        pass


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
        print("Location: " + self.location[0] + ", " + self.location[1])
        print()


class Agent(SimpleProblemSolvingAgentProgram):

    def __init__(self, location, initial_state=None):
        super(Agent, self).__init__(initial_state=None)
        self.location = location

    def update_state(self, percept):
        pass

    def formulate_goal(self, state):
        pass

    def formulate_problem(self, state, goal):
        pass

    def search(self, problem):
        pass


class Solution:

    def __init__(self):
        pass

    @staticmethod
    def parseJSON(filename):
        data_file = open(filename)

        data = json.load(data_file)
        data_file.close()

        expected_n = data[0]['results_found']

        n = 0
        restaurant_list = []
        for n in range(expected_n):

            if 'restaurants' not in data[n]: break
            for i in data[n]['restaurants']:
                restaurant_list.append(RestaurantNode(i['restaurant']['cuisines'],
                                                      i['restaurant']['name'],
                                                      i['restaurant']['R']['res_id'],
                                                      [i['restaurant']['location']['latitude'],
                                                       i['restaurant']['location']['longitude']]
                                                      ))
            n += 1

        print(n)

        for restaurant in restaurant_list:
            restaurant.print()

        return restaurant_list
        # print(json.dumps(data, indent=4, sort_keys=False))


if __name__ == '__main__':
    solution = Solution()
    filename = "dataset/file1.json"
    restaurant_list = solution.parseJSON(filename)

    agent = Agent("Italian")


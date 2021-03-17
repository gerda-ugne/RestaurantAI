import json
import math
from aima3.search import Problem, Node, SimpleProblemSolvingAgentProgram
from aima3.utils import is_in


class ClosestRestaurant(Problem):

    def __init__(self, list_of_restaurants, initial="Italian", goal="Mexican"):
        super().__init__(initial, goal)
        self.list_of_restaurants = list_of_restaurants

    def actions(self, state):

        """Return actions in the current restaurant to:
        - scan the nearby area
        - travel to another restaurant

         The algorithm checks whether there are directions to travel to
         if the area was scanned.

         If there are instances upon scanning, the agent can travel as well.
         """

        available_directions = self.scan
        available_actions = ["scan"]

        if available_directions is not None:
            available_actions.append("travel")

        return available_actions

    def scan(self, state):
        """Input parameter : initial coordinates of a place, a list of locations
            Return : a list of places that are located in the area scanned"""

        restaurant_list_within_area = []

        """The implementation of algorithm using Haversine Formula- identifying a distance between two locations using latitude and longitude, 
        was based on an example from a resource cited below: 
        
        Title: How to find the distance between two lat-long coordinates in Python
        Author:kite.com 
        Date: not stated 
        Availability: https://www.kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
    
        I altered variable names and added a FOR loop. 
        """
        state.location[0] = math.radians(state.location[0])
        state.location[1] = math.radians(state.location[1])
        R = 6373
        for i in self.list_of_restaurants:
            lat2 = math.radians(i.state.location[0])
            lon2 = math.radians(i.state.location[1])

            difference_lat = lat2 - state.location[0]
            difference_lon = lon2 - state.location[1]

            a = math.sin(difference_lat / 2) ** 2 + math.cos(state.location[0]) * math.cos(lat2) * math.sin(
                difference_lon / 2) ** 2

            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

            distance = round(R * c , 2)

        # End of code extract.

            if distance <= 5:  # if the distance from initial location is <= 5 km to the current restaurant
                restaurant_list_within_area.append(i)  # add that restaurant to a list
                print(i.state.name)
                print("Distance " + str(distance) + " km")

        return restaurant_list_within_area

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
            return self.scan(state)

    def value(self, state):
        pass

    def goal_test(self, state):

        if isinstance(self.goal, list):
            return is_in(state.cuisines, self.goal)
        else:
            return state.cuisines == self.goal


class RestaurantNode(Node):
    """Data types:
        - Location is a list containing latitude and longitude"""

    def __init__(self, cuisines, name, ID, location, parent=None, action=None, path_cost=0):
        state = State(name, ID, cuisines, location)
        super().__init__(state, parent, action, path_cost)


class State:

    def __init__(self, name, ID, cuisines, location):
        self.name = name
        self.ID = ID
        self.cuisines = cuisines
        self.location = location

    def print_state(self):
        print("Name: " + self.name)
        print("Cuisines: " + self.cuisines)
        print("ID: " + str(self.ID))
        print("Location: " + self.location[0] + ", " + self.location[1])
        print()


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
                                                      [float(i['restaurant']['location']['latitude']),
                                                       float(i['restaurant']['location']['longitude'])]
                                                      ))
            n += 1

        return restaurant_list
        # print(json.dumps(data, indent=4, sort_keys=False))


if __name__ == '__main__':
    solution = Solution()
    filename = "dataset/file1.json"
    restaurant_list = solution.parseJSON(filename)

    problem = ClosestRestaurant(restaurant_list)
    ClosestRestaurant.list_of_restaurants = restaurant_list

    """ Initial location: 28.554281, 77.19447 which is almost the same as for the first restaurant in the list  """
    problem.scan(restaurant_list[0].state)

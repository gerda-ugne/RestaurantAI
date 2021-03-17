import json
import math
from aima3.search import Problem, Node, SimpleProblemSolvingAgentProgram



class ClosestRestaurant(Problem):
    def __init__(self):
        pass

    def actions(self, state):
        """Return actions in the current restaurant to:
        - scan the nearby area
        - travel to another restaurant """
        raise NotImplementedError

    def scan(self, initial_lat, initial_long, list_of_restaurants):
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
        lat_initial = math.radians(initial_lat)
        lon1_initial = math.radians(initial_long)
        R = 6373
        for i in list_of_restaurants:
            lat2 = math.radians(float(i.location[0]))
            lon2 = math.radians(float(i.location[1]))
            difference_lon = lon2 - lon1_initial
            difference_lat = lat2 - lat_initial

            a = math.sin(difference_lat / 2) ** 2 + math.cos(lat_initial) * math.cos(lat2) * math.sin(difference_lon / 2) ** 2

            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c
        # End of code extract.

            if distance <= 5: # if the distance from initial location is <= 5 km to the current restaurant
                restaurant_list_within_area.append(i) #add that restaurant to a list
                print(i.name)
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

    action1 = ClosestRestaurant()
    """ Initial location: 28.554281, 77.19447 which is almost the same as for the first restaurant in the list  """
    action1.scan(28.5542851, 77.19447, restaurant_list)


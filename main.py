import json
import math
# from aima3.search import Problem, Node, depth_limited_search, uniform_cost_search, Thing,
# astar_search, greedy_best_first_graph_search
import folium as folium
from aima3.search import *


class ClosestRestaurant(Problem):
    # heuristic
    global goal_node

    def __init__(self, list_of_restaurants, initial=None, goal=None):
        super().__init__(initial, goal)
        self.list_of_restaurants = list_of_restaurants
        global goal_node

    def actions(self, state):

        """Return actions in the current restaurant to:
        - scan the nearby area
        - travel to another restaurant

         The algorithm checks whether there are directions to travel to
         if the area was scanned.

         If there are instances upon scanning, the agent can travel as well.
         """

        available_directions = self.scan(state)
        """available_actions = ["scan"]

        if available_directions is not None:
            available_actions.append("travel")"""

        return available_directions

    def scan(self, state):
        """Input parameter : state where the action was initiated
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
        initial_lan = math.radians(state.location[0])
        initial_lon = math.radians(state.location[1])
        R = 6373
        for i in self.list_of_restaurants:
            lat2 = math.radians(i.state.location[0])
            lon2 = math.radians(i.state.location[1])

            difference_lat = lat2 - initial_lan
            difference_lon = lon2 - initial_lon

            a = math.sin(difference_lat / 2) ** 2 + math.cos(initial_lan) * math.cos(lat2) * math.sin(
                difference_lon / 2) ** 2

            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

            distance = round(R * c, 2)

            # End of code extract.

            if distance <= 150:  # if the distance from initial location is <= 5 km to the current restaurant
                restaurant_list_within_area.append(i.state)  # add that restaurant to a list
                # print(i.state.name)
                # print("Distance " + str(distance) + " km")

        return restaurant_list_within_area

    """Returns the updated agent's state after travel"""

    def travel(self, state):
        return state

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        if action is not None:
            return action
        else:
            return state

    def value(self, state):
        pass

    def goal_test(self, state):
        if self.goal in state.cuisines:
            return True
        else:
            return False

    def path_cost(self, c, current_state, action, next_state):
        distance_between_states = 0
        lat_initial = math.radians(current_state.location[0])
        lon_initial = math.radians(current_state.location[1])
        R = 6373
        lat_next = math.radians(next_state.location[0])
        lon_next = math.radians(next_state.location[1])
        difference_lon = lon_next - lon_initial
        difference_lat = lat_next - lat_initial
        a = math.sin(difference_lat / 2) ** 2 + math.cos(lat_initial) * math.cos(lat_next) * math.sin(
            difference_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance_between_states = round(R * c, 2)

        return distance_between_states

    def pre_h(self, cuisine, initial_node):
        """ Finding a goal node
        :param: cuisine: a goal cuisine as a string
        :param: initial node: an initial node's location
        :return: a goal node
        """

        goal_list = []  # a list of all nodes containing goal cuisine
        for x in self.list_of_restaurants:
            if cuisine in x.state.cuisines:
                goal_list.append(x)  # creates a list of restaurants containing the goal cuisine

        distance_from_potential_goal = []  # a list of distances from initial location to goal location
        for x in goal_list:
            i = self.path_cost(0, initial_node.state, "travel", x.state)
            distance_from_potential_goal.append(i)

        # finding the shortest distance
        index_of_smallest_value = distance_from_potential_goal.index(min(distance_from_potential_goal))
        # print(goal_list[index_of_smallest_value].state.name)
        return goal_list[index_of_smallest_value]  # returning a  node that has a shortest distance

    def h(self, node):
        """
        Heuristic function
        :param node: current node
        :return: a float value
        """
        # Using Euclidean distance
        h_value = math.sqrt((node.state.location[0] - goal_node.state.location[0]) ** 2 + (
                node.state.location[1] - goal_node.state.location[1]) ** 2)
        return round(h_value, 2)


class RestaurantNode(Node):
    """Data types:
        - Location is a list containing latitude and longitude"""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)

    def __lt__(self, node):
        return self.path_cost < node.path_cost


class State:

    def __init__(self, cuisines, name, ID, location):
        self.cuisines = cuisines
        self.name = name
        self.ID = ID
        self.location = location

    def print_state(self):
        print("Name: " + self.name)
        print("Cuisines: " + self.cuisines)
        print("ID: " + str(self.ID))
        print("Location: " + str(self.location[0]) + ", " + str(self.location[1]))
        print("\n")

    def __lt__(self, state):
        return self.ID < state.ID


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
                state = (State(i['restaurant']['cuisines'],
                               i['restaurant']['name'],
                               i['restaurant']['R']['res_id'],
                               [float(i['restaurant']['location']['latitude']),
                                float(i['restaurant']['location']['longitude'])]
                               ))
                restaurant_list.append(RestaurantNode(state))
            n += 1

        return restaurant_list
        # print(json.dumps(data, indent=4, sort_keys=False))

    @staticmethod
    def print_answer(answer):
        if answer == "cutoff":
            print("No solution found in the range.")
        elif answer is not None:
            answer.state.print_state()
            print("Distance: " + str(answer.path_cost) + " kms.\n")
        else:
            print("No solution found.")

    @staticmethod
    def plot_map(restaurant_list, goal_node):

        points = []
        for restaurant in restaurant_list:
            points.append(tuple([restaurant.state.location[0], restaurant.state.location[1]]))

        ave_lat = sum(p[0] for p in points) / len(points)
        ave_lon = sum(p[1] for p in points) / len(points)

        goal = tuple([goal_node.state.location[0], goal_node.state.location[1]])

        # Load map centred on average coordinates
        my_map = folium.Map(location=[ave_lat, ave_lon], zoom_start=3)

        # add a markers
        for each in points:
            folium.Marker(each).add_to(my_map)

        #folium.Marker(goal).add_to(my_map)

        # fadd lines
        # folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(my_map)

        # Save map
        my_map.save("./map.html")


if __name__ == '__main__':
    solution = Solution()
    filename = "dataset/file1.json"
    restaurant_list = solution.parseJSON(filename)

    goal_cuisine = "Mughlai"
    problem = ClosestRestaurant(restaurant_list, restaurant_list[0].state, goal_cuisine)

    print("DEPTH LIMITED SEARCH:")
    answer = depth_limited_search(problem, 3)
    solution.print_answer(answer)

    print("UNIFORM COST SEARCH:")
    answer = uniform_cost_search(problem)
    solution.print_answer(answer)

    goal_node = problem.pre_h(goal_cuisine, restaurant_list[0])  # updating a global variable - goal node

    solution.plot_map(restaurant_list, goal_node)
    # print("H value")
    # print(problem.h(restaurant_list[23]))
    # print(problem.h(restaurant_list[1]))

    print("GREEDY SEARCH:")
    answer = greedy_best_first_graph_search(problem, problem.h)
    solution.print_answer(answer)

    print("A STAR SEARCH:")
    answer = astar_search(problem, problem.h)
    solution.print_answer(answer)

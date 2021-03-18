import json
import math
from aima3.search import Problem, Node, SimpleProblemSolvingAgentProgram, depth_limited_search, uniform_cost_search
from aima3.utils import memoize, PriorityQueue


class ClosestRestaurant(Problem):

    def __init__(self, list_of_restaurants, initial=None, goal=None):
        super().__init__(initial, goal)
        self.list_of_restaurants = list_of_restaurants
        if list_of_restaurants is not None:
            self.agent_location = list_of_restaurants[0].state.location
        else:
            self.agent_location = None

    def actions(self, state):

        """Return actions in the current restaurant to:
        - scan the nearby area
        - travel to another restaurant

         The algorithm checks whether there are directions to travel to
         if the area was scanned.

         If there are instances upon scanning, the agent can travel as well.
         """

        available_directions = self.scan
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

            if distance <= 10:  # if the distance from initial location is <= 5 km to the current restaurant
                restaurant_list_within_area.append(i)  # add that restaurant to a list
                print(i.state.name)
                print("Distance " + str(distance) + " km")

        return restaurant_list_within_area

    """Returns the updated agent's state after travel"""

    def travel(self, state):
        return state

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        After scanning: return locations available to travel to
        After travelling: return new coordinates for the agent
        """
        if action == "travel":
            return self.travel(state)
        elif action == "scan":
            return self.scan(state)

    def value(self, state):
        pass

    def goal_test(self, state):
        if self.goal.cuisines in state.cuisines:
            return True
        else:
            return self.goal.cuisines == state.cuisines

    def path_cost(self, c, current_state, action, next_state):
        distance_between_states = 0
        if action == "travel":
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


class RestaurantNode(Node):
    """Data types:
        - Location is a list containing latitude and longitude"""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)


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

    def depth_limited_search(self, problem, limit=50):
        """[Figure 3.17]"""

        def recursive_dls(node, problem, limit):
            if problem.goal_test(node.state):
                return node
            elif limit == 0:
                return 'cutoff'
            else:
                cutoff_occurred = False
                for child in node.expand(problem):
                    result = recursive_dls(child, problem, limit - 1)
                    if result == 'cutoff':
                        cutoff_occurred = True
                    elif result is not None:
                        return result
                return 'cutoff' if cutoff_occurred else None

        # Body of depth_limited_search:
        return recursive_dls(RestaurantNode(problem.initial), problem, limit)

    def best_first_graph_search(self, problem, f, display=False):
        """Search the nodes with the lowest f scores first.
        You specify the function f(node) that you want to minimize; for example,
        if f is a heuristic estimate to the goal, then we have greedy best
        first search; if f is node.depth then we have breadth-first search.
        There is a subtlety: the line "f = memoize(f, 'f')" means that the f
        values will be cached on the nodes as they are computed. So after doing
        a best first search you can examine the f values of the path returned."""
        f = memoize(f, 'f')
        node = Node(problem.initial)
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()
        while frontier:
            node = frontier.pop()
            if problem.goal_test(node.state):
                if display:
                    print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                return node
            explored.add(node.state)
            for child in node.expand(problem):
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)
        return None

    def uniform_cost_search(self, problem):
        """[Figure 3.14]"""
        return self.best_first_graph_search(problem, lambda node: node.path_cost)


if __name__ == '__main__':
    solution = Solution()
    filename = "dataset/file1.json"
    restaurant_list = solution.parseJSON(filename)

    problem = ClosestRestaurant(restaurant_list, restaurant_list[0].state, restaurant_list[54].state)
    # problem.scan(restaurant_list[0].state)

    solution.depth_limited_search(problem, 1)
    # solution.uniform_cost_search(problem)

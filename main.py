from aima.search import Problem, Node


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
        raise NotImplementedError


class RestaurantNode(Node):

    def __init__(self, state, id, location, parent=None, action=None, path_cost=0):
        super(RestaurantNode, self).__init__()
        self.id = id
        self.location = location

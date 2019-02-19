""" Library for building and using undirected graphs. It defines a generic Graph class and its methods

    A graph G(N, L) is a collection of nodes (also called vertices) that connect to each other using
    links (also called edges). A graph is called connected if there are no isolated nodes. A graph
    is called undirected if all links are bi-directional. A graph is called simple if it does not have
    links from a node to the same node, and if there can be at most one link from node to node.

    This library supports simple undirected graphs (connected or non-connected).

    In this implementation a graph is defined as a dictionary with the node ID as the key. Each key
    is associated with a list of neighbors and a payload.
"""

import copy
import json

__author__ = "Edwin Heredia"
__copyright__ = "Copyright 2019"
__license__ = "Not ready for distribution"
__version__ = "0.1.0"
__status__ = "In development"

DEFAULT_INDENT = 4  # Default indent size for pretty format of saved data
BASE_NODE_DATA = {'near': set(), 'payload': None}


class Graph(object):
    def __init__(self):
        # Define private variables
        self.__data = {}     # dictionary object that maps a node with neighbors and payload

    def size(self):
        """ Provides the number of nodes in the graph """
        return len(self.__data)

    def node_exists(self, node_id):
        """ Verifies if a node identified by an ID (integer or string) already exists in the graph.
        Returns True if node exists or False otherwise.
        """
        if node_id in self.__data.keys():
            return True
        else:
            return False

    def node_does_not_exist(self, node_id):
        """ Checks if a node (identified by its ID) does not exist in the graph. Returns True if
        the node does not exist or False if it exist.
        """
        return False if self.node_exists(node_id) else True

    def has_payload(self, node_id):
        """ Verifies if a node identified by an ID (integer or string) has a payload. Returns True if a payload
        has been added to the node.
        """
        return self.retrieve_payload(node_id) is not None

    def link_exists(self, init_id, dest_id):
        """ Verifies if a certain link between two nodes (identified by their IDs) already exists in the graph.
        Returns True if the link exists. Returns False if the link does not exist or if any of the nodes do not
        exist.
        """
        if self.node_exists(init_id) and self.node_exists(dest_id):
            links1 = self.__data[init_id]['near']
            links2 = self.__data[dest_id]['near']

            if dest_id in links1 and init_id in links2:
                return True
            else:
                return False
        else:
            return False

    def link_does_not_exist(self, init_id, dest_id):
        """ Checks if a link does not exist between two nodes (identified by their IDs). Returns
        True if the link does not exist.
        """
        return False if self.link_exists(init_id, dest_id) else True

    def get_nodes(self):
        """ Returns the list of all nodes (identified by their IDs) in the graph
        """
        return self.__data.keys()

    def get_links(self, node_id):
        """ Returns a list of neighbor nodes for a node identified by its ID (string or integer).
        Returns None if the target node does not exist in the graph.
        """
        if self.node_exists(node_id):
            return self.__data[node_id]["near"]
        else:
            return None

    def add_node(self, node_id):
        """ Adds a node (identified by its string or integer ID) to the graph without any links.
        Returns the number of added nodes (zero or one).
        """
        if self.node_does_not_exist(node_id):
            self.__data[node_id] = copy.deepcopy(BASE_NODE_DATA)
            return 1
        else:
            return 0

    def add_nodes_from_list(self, node_list):
        """ Adds a group of nodes from a list (each node defined by its string or integer ID).
        Returns the number of added nodes. A graph cannot have duplicate nodes. If the list has
        IDs that alreay exist or duplicates, they are ignored.
        """
        added_nodes = 0
        for nd in node_list:
            result = self.add_node(nd)
            added_nodes += result
        return added_nodes

    def remove_link(self, init_id, dest_id):
        """ Removes a link between two nodes identified by their string or integer IDs. Returns the
        number of links removed.
        """
        if self.link_exists(init_id, dest_id):
            self.__data[init_id]['near'].remove(dest_id)
            self.__data[dest_id]['near'].remove(init_id)
            return 1
        else:
            return 0

    def remove_node(self, node_id):
        """ Removes an existing node (defined by a string or integer ID) from the graph. Returns the
        number of removed nodes.
        """
        if self.node_exists(node_id):
            # Get all neighbor nodes
            nbors = copy.deepcopy(self.__data[node_id]['near'])

            # Remove links between the selected nodes and its neighbors
            for nb in nbors:
                self.remove_link(node_id, nb)

            # Remove the node entry from the graph
            del self.__data[node_id]

            return 1
        else:
            return 0

    def remove_nodes_from_list(self, node_list):
        """ Removes nodes from a node list (each node identified by its ID; a string or integer).
        Returns the number of removed nodes.
        """
        for nd in node_list:
            self.remove_node(nd)

    def add_link(self, init_id, dest_id):
        """ Adds a link between two nodes identified by their string or integer IDs.
        Returns number of added links. It can be 0 if any of the two nodes does not exist.
        """
        if self.node_exists(init_id) and self.node_exists(dest_id):
            self.__data[init_id]['near'].add(dest_id)
            self.__data[dest_id]['near'].add(init_id)
            return 1
        else:
            return 0

    def add_links_from_list(self, link_list):
        """ Adds a list of links to the graph. The list contains tuples with each tuple defining
        a link between two nodes. Returns the number of links added.
        """
        count = 0
        for edge in link_list:
            result = self.add_link(edge[0], edge[1])
            count += result
        return count

    def remove_links_from_list(self, link_list):
        """ Removes a list of links from the graph. The list contains tuples with each tuple
        defining a link between two nodes. Returns the number of removed links.
        """
        count = 0
        for edge in link_list:
            result = self.remove_link(edge[0], edge[1])
            count += result
        return count

    def retrieve_payload(self, node_id):
        """ Retrieves and returns the payload from a node identified by its ID (string or integer).
        Returns None if node does not exist or if node does not have any payload.
        """
        return None if self.node_does_not_exist(node_id) else self.__data[node_id]["payload"]

    def retrieve_neighbors(self, node_id):
        """ Retrieves the list of neighbors for a node identified by its string or integer ID.
        If the node does not exist the result is None. If the node exists but it has no neighbors
        the result is an empty list. Notice that this function returns a List object (not a set object).
        """
        return None if self.node_does_not_exist(node_id) else list(self.__data[node_id]["near"])

    def retrieve_node_data(self, node_id):
        """ Retrieves neighbors and payload for a node identified by its ID (string or integer).
        If the node does not exist, both returned values are set to None. If the payload does not
        exist, the returned payload value is set to None. If the node does not have any neighbors,
        the returned neighbors value shows an empty list.
        """
        if self.node_does_not_exist(node_id):
            return None
        else:
            return self.__data[node_id]['near'], self.__data[node_id]['payload']

    def add_payload(self, node_id, payload):
        """ Adds a payload to a node identified by its string or integer ID. The payload can be
        any Python data type (except NoneType). Returns 0 if the node does not exist or 1
        if it successfully added a payload.
        """
        if self.node_does_not_exist(node_id) or payload is None:
            return 0
        else:
            self.__data[node_id]['payload'] = payload
            return 1

    def __str__(self):
        """ Returns a string displaying graph information for use in print statements.
        """
        text_mode = ""
        nodes = self.get_nodes()
        for nd in nodes:
            nbors, pload = self.retrieve_node_data(nd)
            text_mode += "node: {},  near: {},  payload: {}\n".format(nd, nbors, pload)

        return text_mode

    def dfs_traverse(self, init_id):
        """Use the Depth-First Search (DFS) algorithm for graph traversal starting with a node
        defined by its string or integer ID (init_id). Returns a list of visited nodes in the order
        in which they have been visited.
        """

        visited = [init_id]
        path = [init_id]
        self.__rec_dfs_traverse(init_id, visited, path)
        return visited

    def __rec_dfs_traverse(self, current, visited, path):
        """ (Private method) Process graph node and continue to next node recursively
        using the DFS strategy. The input arguments are:
            current: The current node ID which is being processed
            visited: A list of visited nodes
            path: A list of nodes representing the traversal path
        """

        # define when to terminate recursion
        if len(path) == 0:
            return

        # determine the links (edges) for the current node
        links = self.retrieve_neighbors(current)

        # determine if any of the links has not been visited
        found = False
        selected = None
        for link in links:
            if link not in visited:
                found = True
                selected = link
                break

        # If a link has not been visited then vist the node and repeat process (recursion)
        if found:
            visited.append(selected)
            path.append(selected)
            self.__rec_dfs_traverse(selected, visited, path)

        # If all links have been visited then backtrack to previous entry in path and repeat process (recursion)
        else:
            path.pop()
            if len(path) != 0:
                new_current = path[len(path) - 1]
            else:
                new_current = None  # If the path is empty there is no current node

            self.__rec_dfs_traverse(new_current, visited, path)

    def bfs_traverse(self, init_id):
        """ Use the Breadth-First Search (BFS) algorithm for graph traversal starting from a node identified by
        its string or integer ID (init_id). Returns a list of visited nodes in the order in which they have
        been visited
        """

        visited = [init_id]
        stack = [init_id]
        self.__rec_bfs_traverse(visited, stack)
        return visited

    def __rec_bfs_traverse(self, visited, stack):
        """ (Private method) Process graph node and continue to next node recursively using the BFS strategy.
        The input arguments are:
            visited: A list of visited nodes identified by their IDs
            stack: A list of nodes representing the processed nodes
        """

        # define when to terminate recursion
        if len(stack) == 0:
            return

        # get current working node from a LIFO stack and find its neighbors
        current = stack.pop()
        links = self.retrieve_neighbors(current)

        # find the subset of neighbors that have not yet been visited
        unvisited = []
        for link in links:
            if link not in visited:
                unvisited.append(link)

        # add univisted neighbors to the visited list and to the stack
        if len(unvisited) != 0:
            for unv in unvisited:
                visited.append(unv)
                stack.append(unv)
            self.__rec_bfs_traverse(visited, stack)
        # if there are no unvisited neighbors then continue recursion
        else:
            self.__rec_bfs_traverse(visited, stack)

    def save_json(self, filepath, pretty=True):
        """ Saves graph data as a text file to the file whose path is given by filepath. Uses
        a json format with readable blank spaces (pretty is True) or without blank spaces (pretty is False).
        """
        with open(filepath, "w") as jf:
            if pretty:
                json.dump(self.__do_serializable(), jf, ensure_ascii=False, indent=DEFAULT_INDENT, sort_keys=True)
            else:
                json.dump(self.__do_serializable(), jf, ensure_ascii=False, sort_keys=True)

    def load_json(self, filepath):
        """ Loads graph data from a text file (json format) whose file is given by filepath.
        """
        with open(filepath, "r") as jf:
            recovered_data = json.load(jf)
        self.__undo_serializable(recovered_data)

    def __do_serializable(self):
        """ Takes graph data and converts into a dictionary that can be json-serialized for storage.
        Returns the output dictionary.
        """
        data_clone = copy.deepcopy(self.__data)
        for nd in data_clone.keys():
            data_clone[nd]['neighbors'] = list(data_clone[nd]['near'])
            del data_clone[nd]['near']
        return data_clone

    def __undo_serializable(self, recovered_dict):
        """ Takes a dictionary from saved data (recovered_dict) and loads the dictionary as graph data. """
        self.__data = copy.deepcopy(recovered_dict)
        for nd in self.__data.keys():
            self.__data[nd]['near'] = set(recovered_dict[nd]['neighbors'])
            del self.__data[nd]['neighbors']

    def is_connected_graph(self, init_id):
        """ Determines if the graph is a fully connected graph, i.e. it has no isolated nodes.
        Starts the test from a node identified by its ID (init_id). Returns True or False.
        """
        visited = self.dfs_traverse(init_id)
        return True if len(visited) == self.size() else False

    def get_depth_layer(self, node_id, layer):
        """ Returns the list of nodes at a certain depth level (layer) from the start node (identified
        by node_id). The start node is at layer 0, one-hop nodes are layer 1, two-hop nodes are layer 2,
        and so forth.
            The result is a dictionary object with a 'layer' and 'nodes' keys . The layer value
        shows the maximum layer reached during the search. The value of the 'nodes' key contains the
        list of nodes at such layer.
        """
        if layer == 0:
            return {'layer': 0, 'nodes': [node_id]}

        finished = False
        layer_nodes = [node_id]
        visited = [node_id]
        layer_count = 0

        while not finished:
            layer_count += 1
            new_layer_nodes = []

            for nd in layer_nodes:
                for nid in self.retrieve_neighbors(nd):
                    if nid not in visited:
                        visited.append(nid)
                        new_layer_nodes.append(nid)

            if len(new_layer_nodes) == 0:
                finished = True
                layer_count -= 1

            elif layer_count == layer:
                finished = True
                layer_nodes = new_layer_nodes

            else:
                layer_nodes = new_layer_nodes

        response = {'layer': layer_count,
                    'nodes': layer_nodes}

        return response

    def is_node_in_layer(self, start_node, target_node, layer):
        """ Checks if a target node exists at a given depth layer from a start node. The nodes are
        identified by their IDs (string or integer). The layer is an integer with 0 being the starting
        layer.
            Returns True if the target node is at the specified layer or False otherwise. If the nodes
            are not graph members the function returns False.
        """
        if self.node_does_not_exist(start_node) or self.node_does_not_exist(target_node):
            return False

        result = self.get_depth_layer(start_node, layer)

        if result["layer"] < layer:
            return False
        else:
            if target_node in result["nodes"]:
                return True
            else:
                return False

    def shortest_path(self, init_id, dest_id):
        """ Use a Breadth-First Search (BFS) strategy to obtain the shortest path between an initial node
        and a destination node.
            Returns a list of nodes defining the shortest path between the two nodes. If any of the nodes
        does not exist, it returns an empty list.
        """

        if self.node_does_not_exist(init_id) or self.node_does_not_exist(dest_id):
            return []

        if init_id == dest_id:
            return [init_id]

        # Initialize map of layers
        layer_count = 0
        vis_map = {init_id: layer_count}

        finished = False
        layer_nodes = [init_id]

        # Iterate through the graph to tag each node with a layer value
        while not finished:
            layer_count += 1
            new_layer_nodes = []

            for nd in layer_nodes:
                for nid in self.retrieve_neighbors(nd):
                    if nid not in vis_map.keys():
                        vis_map[nid] = layer_count
                        new_layer_nodes.append(nid)

            if len(new_layer_nodes) == 0:
                finished = True
                layer_count -= 1

            else:
                layer_nodes = new_layer_nodes

        # Backtrack from destination to initial node to find path
        current = dest_id
        node_path = [dest_id]
        counter = 0
        while current != init_id and counter < 1000:
            nbors = self.retrieve_neighbors(current)

            min_layer = self.size() + 1  # large number that exceeds max layer value
            best_parent = None
            for nd in nbors:
                if vis_map[nd] < min_layer:
                    min_layer = vis_map[nd]
                    best_parent = nd

            node_path.append(best_parent)
            current = best_parent
            counter += 1

        # Return reversed path
        return node_path[::-1]


if __name__ == "__main__":
    gr = Graph()

    for k in range(7):
        gr.add_node(k)

    gr.add_link(0, 3)
    gr.add_link(0, 2)
    gr.add_link(2, 4)
    gr.add_link(0, 1)
    gr.add_link(1, 5)
    gr.add_link(5, 4)
    gr.add_link(5, 6)
    gr.add_link(3, 4)
    gr.add_link(1, 6)

    gr.add_payload(0, 0.12)
    gr.add_payload(1, 1.12)
    gr.add_payload(2, 2.12)

    print(gr)

    print("Traverse graph starting from node 0 using DFS: ")
    visited1 = gr.dfs_traverse(0)
    print("DFS visited nodes: {}".format(visited1))

    print("Traverse graph starting from node 0 using BFS: ")
    visited2 = gr.bfs_traverse(0)
    print("BFS visited nodes: {}".format(visited2))

    print("**********************************")

    output_file = "tempfile.json"
    gr.save_json(output_file)
    print("graph data saved to {}".format(output_file))

    print("-------------------------------------")

    grnew = Graph()
    grnew.load_json(output_file)

    print(grnew)
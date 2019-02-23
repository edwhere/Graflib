""" Library for building and using undirected graphs. It defines a generic Graph class and its methods

    A graph G(N, L, W) is a collection of nodes N (also called vertices) that connect to each other using
    links L (also called edges). Links can have weights W.

    This implementation admits graphs with or without weights.

    A graph is called connected if there are no isolated nodes. A graph is called undirected if all
    links are bi-directional. A graph is called simple if it does not have links from a node to the same
    node, and if there can be at most one link from node to node.

    This library supports simple undirected graphs (connected or non-connected).

    In this implementation a graph is defined as a dictionary with the node ID as the key. Each key
    is associated with a list of neighbors, weights, and a payload.

    Important terminology and definitions:
    A node is always referenced by a node ID, which is a string or integer
    Two nodes are neighbors if there is a link that connects the nodes
    A link is defined as a 2-element tuple (node_1, node_2) for graphs with no weights
    A link is defined as a 3-element tuple (node_1, node_2, weight) for graphs with weights

    Functions that take a link as input allow a 2-element link for graphs with weights with a default
    weight of 1.0

    Functions that take a link as input allow a 3-element link for graphs with no weights. The third
    element is simply ignored.

"""

import copy
import json

__author__ = "Edwin Heredia"
__copyright__ = "Copyright 2019"
__version__ = "0.1.0"

DEFAULT_INDENT = 4  # Default indent size for saving data using a pretty format
BASE_NODE_DATA = {'near': set(), 'payload': None}


class Graph(object):
    def __init__(self, has_weights=False):
        # Define private variables
        self.__has_weights = has_weights
        self.__data = {}     # dictionary object that maps a node with neighbors and payload

    def size(self):
        """ Provides the number of nodes in the graph """
        return len(self.__data)

    def get_nodes(self):
        """ Returns the list of all nodes (identified by their IDs) in the graph
        """
        return self.__data.keys()

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

    def payload_exist(self, node_id):
        """ Verifies if a node identified by an ID (integer or string) has a payload. Returns True if a payload
        has been added to the node.
        """
        return self.get_payload(node_id) is not None

    def payload_does_not_exist(self, node_id):
        """ Checks if a node identified by its ID contains no payload. Returns True if payload has not been
        added to the node.
        """
        return False if self.payload_exist(node_id) else True

    def are_neighbors(self, init_id, dest_id):
        """ Verifies and returns True if two nodes are neighbors in the graph.
        Returns False if they are not neighbors or if any of the nodes does not exist.
        """
        if self.node_exists(init_id) and self.node_exists(dest_id):
            nbors1 = [elem[0] for elem in self.__data[init_id]['near']]
            nbors2 = [elem[0] for elem in self.__data[dest_id]['near']]

            if dest_id in nbors1 and init_id in nbors2:
                return True
            else:
                return False
        else:
            return False

    def are_not_neighbors(self, init_id, dest_id):
        """ Verifies and returns True if two nodes are not neighbors in the graph.
        """
        return False if self.are_neighbors(init_id, dest_id) else True

    def get_links(self, node_id):
        """ Returns a list of links for a node identified by its ID (string or integer).
        If the graph has no weights, it returns a list of tuples of the form (node_id, next_id).
        If it is a weighted graph, it returns a list of tuples of the form (node_id, next_id, weight).
        Returns None if the target node does not exist in the graph.
        """
        if self.node_does_not_exist(node_id):
            return None
        else:
            graph_links = self.__data[node_id]['near']
            if self.__has_weights:
                return [(node_id, elem[0], elem[1]) for elem in graph_links]
            else:
                return [(node_id, elem[0]) for elem in graph_links]

    def get_neighbors(self, node_id):
        """ Returns a list of neighbor nodes for a node identified by its ID (string or integer).
        The list contains only neighbor nodes and not link weights. Returns None if the target node does not exist.
        """
        if self.node_exists(node_id):
            return [link[1] for link in self.get_links(node_id)]
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

    def __get_reference_tuple(self, init_id, dest_id):
        """ Private method to extract the tuple that represents the link between the init_id and dest_id nodes.
        If the link exists, the response is a tuple of the form (dest_id, weight). If the graph has no weights,
        the weight value is set to None. If the link does not exist this method returns None.
        """
        if self.are_neighbors(init_id, dest_id):
            all_tuples = self.__data[init_id]['near']
            for tuple in all_tuples:
                if tuple[0] == dest_id:
                    return tuple
            return None
        else:
            return None

    def remove_link_between_nodes(self, init_id, dest_id):
        """ Removes a link between two nodes identified by their IDs. Returns the
        number of links removed (0 or 1).
        """
        if self.are_neighbors(init_id, dest_id):
            tuple_forward = self.__get_reference_tuple(init_id, dest_id)
            tuple_backward = self.__get_reference_tuple(dest_id, init_id)

            if tuple_forward is None or tuple_backward is None:
                return 0
            else:
                self.__data[init_id]['near'].remove(tuple_forward)
                self.__data[dest_id]['near'].remove(tuple_backward)
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
            nbors = [nbor[0] for nbor in nbors]

            # Remove links between the selected nodes and its neighbors
            for nb in nbors:
                self.remove_link_between_nodes(node_id, nb)

            # Remove the node entry from the graph
            del self.__data[node_id]

            return 1
        else:
            return 0

    def remove_nodes_from_list(self, node_list):
        """ Removes nodes from a node list (each node identified by its ID; a string or integer).
        Returns the number of removed nodes.
        """
        count = 0
        for nd in node_list:
            res = self.remove_node(nd)
            count += res
        return count

    def add_link(self, init_id, dest_id, weight=None):
        """ Adds a link between two nodes identified by their IDs and optionally a weight value.
        If the graph has defined as having weights:
           The weight value is assigned to the link. If no weight is given, the default is 1.0
        If the graph has not been defined as having weights:
           The weight value is ignored

        Returns number of added links. It can be 0 if any of the two nodes does not exist.
        """
        if self.node_exists(init_id) and self.node_exists(dest_id):
            if self.__has_weights:
                tuple_forward = (dest_id, 1.0) if weight is None else (dest_id, weight)
                tuple_backward = (init_id, 1.0) if weight is None else (init_id, weight)
            else:
                tuple_forward = (dest_id, None)
                tuple_backward = (init_id, None)

            self.__data[init_id]['near'].add(tuple_forward)
            self.__data[dest_id]['near'].add(tuple_backward)
            return 1
        else:
            return 0

    def add_links_from_list(self, link_list):
        """ Adds a list of links to the graph. The list can contains  2-element or 3-element tuples:
                             (init_id, dest_id) or (init_id, dest_id, weight)
        If the Graph has weights, then
               A 2-element tuple defines a link with a default weight of 1.0
               A 3-element tuple defines a link with a given weigth
        If the Graph has no weights, then
               A 2-element tuple defines a link
               In a 3-element tuple, the third element is ignored

        Returns the number of links added.
        """

        if self.__has_weights:
            count = 0
            for edge in link_list:
                e0, e1 = edge[0], edge[1]
                result = self.add_link(e0, e1, 1.0) if len(edge) == 2 else self.add_link(e0, e1, edge[2])
                count += result
            return count
        else:
            count = 0
            for edge in link_list:
                result = self.add_link(edge[0], edge[1])
                count += result
            return count

    def remove_links_from_list_of_neighbors(self, neighbors_list):
        """ Removes links defined by a list of neighbors. Each element in the list is a tuple of the
        form: (node_1_id, node_2_id). The graph link is removed only if the two nodes in a tuple are
        actually neighbors. Returns the number of removed links.
        """
        count = 0
        for nbor_tuple in neighbors_list:
            result = self.remove_link_between_nodes(nbor_tuple[0], nbor_tuple[1])
            count += result
        return count

    def get_payload(self, node_id):
        """ Retrieves and returns the payload from a node identified by its ID (string or integer).
        Returns None if node does not exist or if node does not have any payload.
        """
        return None if self.node_does_not_exist(node_id) else self.__data[node_id]["payload"]

    def retrieve_node_data(self, node_id):
        """ Retrieves neighbors and payload for a node identified by its ID (string or integer).
        If the node does not exist, both returned values are set to None. If the payload does not
        exist, the returned payload value is set to None. If the node does not have any neighbors,
        the returned neighbors value shows an empty list.
        """
        return self.get_neighbors(node_id), self.get_links(node_id)

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

    def add_payloads_from_list(self, payload_list):
        """ Adds payloads from a list. Each element of the list is a tuple of the form:
                        (node_id, payload)
            Returns the number of successful additions
        """
        count = 0
        for elem in payload_list:
            res = self.add_payload(elem[0], elem[1])
            count += res
        return count

    def remove_payload(self, node_id):
        """ Removes a payload from a node. Returns number of removed payloads (0 or 1).
        A payload is not removed if the node does not exist.
        """
        if self.node_does_not_exist(node_id):
            return 0
        else:
            self.__data[node_id]['payload'] = None
            return 1

    def remove_payloads_from_list(self, payload_list):
        """ Removes payloads defined in a list of nodes. Returns the number of removed payloads.
        A payload is not removed if the node does not exist.
        """
        count = 0
        for nd in payload_list:
            res = self.remove_payload(nd)
            count += res
        return count

    def has_payload(self, node_id):
        """ Returns True if a payload has been added to the node defined by its ID. Returns False
        if the node does not exist or if there is no payload.
        """
        if self.node_does_not_exist(node_id):
            return False
        else:
            return False if self.__data[node_id]['payload'] is None else True

    def __str__(self):
        """ Returns a string displaying graph information for use in print statements.
        """
        text_mode = ""
        nodes = self.get_nodes()
        for nd in nodes:
            links = self.get_links(nd)
            pload = self.get_payload(nd)
            text_mode += "node: {},  near: {},  payload: {}\n".format(nd, links, pload)

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
        links = self.get_neighbors(current)

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
        links = self.get_neighbors(current)

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

    def save_json(self, filepath, pretty=False):
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
            nb_list = list(data_clone[nd]['near'])
            nb_list_of_lists = [list(elem) for elem in nb_list]
            data_clone[nd]['neighbors'] = nb_list_of_lists
            del data_clone[nd]['near']
        return data_clone

    def __undo_serializable(self, recovered_dict):
        """ Takes a dictionary from saved data (recovered_dict) and loads the dictionary as graph data. """
        self.__data = copy.deepcopy(recovered_dict)
        for nd in self.__data.keys():
            list_of_tuples = [tuple(elem) for elem in recovered_dict[nd]['neighbors']]
            self.__data[nd]['near'] = set(list_of_tuples)
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
        list of nodes at such a layer.
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
                for nid in self.get_neighbors(nd):
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
            return True if target_node in result["nodes"] else False

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
                for nid in self.get_neighbors(nd):
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
            nbors = self.get_neighbors(current)

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
    gr.add_payload(5, {'first': 'bob', 'last': 'harris'})

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

    print("=====TESTS ====")

    gr2 = Graph(has_weights=True)

    for k in range(5):
        gr2.add_node(k)

    gr2.add_link(0, 1, 5.5)
    gr2.add_link(0, 2, 6.6)
    gr2.add_link(2, 3, 8.8)

    print(gr2)
    print(gr2.get_links(2))

    print(gr.get_payload(5)['first'])

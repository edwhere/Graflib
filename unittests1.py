""" Defines unit tests for the Graph library.
Running tests from command line requires:
     pip install nose2
     python unittest1.py
"""

import unittest
import graflib as glib


class TestGraflib(unittest.TestCase):

    @staticmethod
    def create_test_graph(type):
        gr_nw = glib.Graph()
        gr_ww = glib.Graph(has_weights=True)

        links_1st = [(0, 1), (0, 2), (2, 3), (1, 3), (1, 4), (3, 4), (2, 4)]
        links_2nd = [(0, 3), (0, 2), (2, 4), (0, 1), (1, 5), (5, 4), (5, 6), (3, 4), (1, 6)]
        links_3rd = [(0, 1, 0.1), (0, 2, 0.2), (2, 3, 2.3), (1, 3, 1.3), (1, 4, 1.4), (3, 4, 3.4), (2, 4, 2.4)]
        links_4th = [(0, 3, 0.3), (0, 2, 0.2), (2, 4, 2.4), (0, 1, 0.1), (1, 5, 1.5),
                     (5, 4, 5.4), (5, 6, 5.6), (3, 4, 3.4), (1, 6, 1.6)]

        payloads = [(0, 100), (1, 101), (2, 102), (3, 103)]

        if type == "nw_5":
            # Graph with 5 nides and no weights
            for k in [0, 1, 2, 3, 4]:
                gr_nw.add_node(k)
            gr_nw.add_links_from_list(links_1st)
            gr_nw.add_payloads_from_list(payloads)
            return gr_nw

        elif type == "nw_7":
            # Graph with 7 nodes and no weights
            for k in [0, 1, 2, 3, 4, 5, 6]:
                gr_nw.add_node(k)
                gr_nw.add_links_from_list(links_2nd)
                gr_nw.add_payloads_from_list(payloads)
                return gr_nw

        elif type == "ww_5":
            # Graph with 5 nodes and weights
            for k in range(5):
                gr_ww.add_node(k)
            gr_ww.add_links_from_list(links_3rd)
            gr_ww.add_payloads_from_list(payloads)
            return gr_ww

        elif type == "ww_7":
            # Graph with 7 nodes and weights
            for k in range(7):
                gr_ww.add_node(k)
            gr_ww.add_links_from_list(links_4th)
            gr_ww.add_payloads_from_list(payloads)
            return gr_ww

        else:
            return None


    def setUp(self):
        super(TestGraflib, self).setUp()
        self.gr_nw_5 = self.create_test_graph(type="nw_5")
        self.gr_nw_7 = self.create_test_graph(type="nw_7")
        self.gr_ww_5 = self.create_test_graph(type="ww_5")
        self.gr_ww_7 = self.create_test_graph(type="ww_7")
        
    def tearDown(self):
        super(TestGraflib, self).tearDown()
        self.gr_nw_5 = None
        self.gr_nw_7 = None
        self.gr_ww_5 = None
        self.gr_ww_7 = None

    def test_create_graph(self):
        my_graph = glib.Graph()
        self.assertEqual(my_graph.size(), 0, "Graph should return a size 0 upon initialization")

    def test_graph_size(self):
        gr = glib.Graph()

        for k in range(4):
            gr.add_node(k)

        self.assertEqual(gr.size(), 4, "Graph should have a size of 4")

        gr.add_node(10)
        gr.add_node(11)

        self.assertEqual(gr.size(), 6, "Graph should have a size of 6")

    def test_node_existence(self):
        gr = glib.Graph()

        for k in range(4):
            gr.add_node(k)

        for k in range(4):
            self.assertTrue(gr.node_exists(k), "Graph should report that node {} exists".format(k))
            self.assertFalse(gr.node_does_not_exist(k),
                             "Graph should report as False the fact that node {} does not exist".format(k))

        for k in range(8, 12):
            self.assertFalse(gr.node_exists(k), "Graph should report that node {} does not exist".format(k))
            self.assertTrue(gr.node_does_not_exist(k),
                            "Graph should report as False the fact that node {} exists".format(k))

    def test_node_list(self):
        res1 = self.gr_nw_5.get_nodes()
        res2 = self.gr_ww_7.get_nodes()

        for k in range(5):
            self.assertIn(k, res1, "Node list should include node {} in graph with no weights".format(k))

        for k in range(7):
            self.assertIn(k, res2, "Node list should include node {} in graph with weights".format(k))

    def test_add_links(self):
        res1 = self.gr_nw_5.get_links(0)
        self.assertEqual(len(res1), 2, "Node 0 shoudl report 2 links in graph with no weights")
        self.assertIn((0, 1), res1, "(0, 1) should be listed as a link for Node 0 in graph with no weights")
        self.assertIn((0, 2), res1, "(0, 2) should be listed as a link for Node 0 in graph with no weights")

        res2 = self.gr_nw_5.get_links(4)
        self.assertEqual(len(res2), 3, "Node 4 should report 3 links in graph with no weights")
        self.assertIn((4, 1), res2, "(4, 1) should be listed as a link for Node 4 in graph with no weights")
        self.assertIn((4, 2), res2, "(4, 2) should be listed as a link for Node 4 in graph with no weights")
        self.assertIn((4, 3), res2, "(4, 3) should be listed as a link for Node 4 in graph with no weights")

        res3 = self.gr_ww_7.get_links(1)
        self.assertEqual(len(res3), 3, "Node 1 should report 3 links in graph with weights")
        self.assertIn((1, 0, 0.1), res3, "(1, 0, 0.1) should be listed as a link for Node 1 in graph with weights")
        self.assertIn((1, 5, 1.5), res3, "(1, 5, 1.5) should be listed as a link for Node 1 in graph with weights")
        self.assertIn((1, 6, 1.6), res3, "(1, 6, 1.6) should be listed as a link for Node 1 in graph with weights")

    def test_remove_links(self):
        self.assertEqual(self.gr_nw_5.size(), 5, "Graph with no weights should report 5 nodes")

        self.assertIn(2, self.gr_nw_5.get_neighbors(4),
                      "Node 2 shoudl be listed as neighbor of 4 in graph with no weights")
        self.assertIn(4, self.gr_nw_5.get_neighbors(2),
                      "Node 4 should be listed as neighbor of 2 in graph with no weights")

        self.gr_nw_5.remove_link_between_nodes(2, 4)

        self.assertNotIn(2, self.gr_nw_5.get_neighbors(4),
                         "Node 2 should not be a neighbor of 4 in graph with no weights")
        self.assertNotIn(4, self.gr_nw_5.get_neighbors(2),
                         "Node 4 should not be a neighbor of 2 in graph with no weights")

        self.assertEqual(self.gr_ww_7.size(), 7, "Graph with weights should report 7 nodes")

        self.assertIn(5, self.gr_ww_7.get_neighbors(4),
                      "Node 5 should be listed as a neighbor of 5 in graph with weights")

        self.assertIn(4, self.gr_ww_7.get_neighbors(5),
                      "Node 5 should be listed as neighbor of 4 in graph with weights")

        self.gr_ww_7.remove_link_between_nodes(4, 5)

        self.assertNotIn(5, self.gr_ww_7.get_neighbors(4),
                         "Node 5 should not be a neighbor of 4 in graph with weights")

        self.assertNotIn(4, self.gr_ww_7.get_neighbors(5),
                         "Node 4 should not be a neighbor of 5 in graph with weights")

    def test_remove_node(self):
        self.assertEqual(self.gr_nw_5.size(), 5, "Graph with no weights should report 5 nodes")
        self.assertIn(1, self.gr_nw_5.get_neighbors(0),
                      "Node 1 should be listed as neighbor of 0 in graph with no weights")
        self.assertIn(0, self.gr_nw_5.get_neighbors(1),
                      "Node 0 should be listed as neighbor of 1 in graph with no weights")
        self.assertIn(2, self.gr_nw_5.get_neighbors(0),
                      "Node 2 should be listed as neighbor of 0 in graph with no weights")
        self.assertIn(0, self.gr_nw_5.get_neighbors(2),
                      "Node 0 should be listed as neighbor of 2 in graph with no weights")

        self.gr_nw_5.remove_node(0)

        self.assertEqual(self.gr_nw_5.size(), 4, "Graph with no weights should report 4 nodes")
        self.assertFalse(self.gr_nw_5.node_exists(0), "Graph with no weights should report that node 0 does not exist")
        self.assertNotIn(0, self.gr_nw_5.get_neighbors(1),
                         "Node 0 should NOT be listed as neighbor of 1 in graph with no weights")
        self.assertNotIn(0, self.gr_nw_5.get_neighbors(2),
                         "Node 0 should NOT be listed as neighbor of 2 in graph with no weights")

        self.assertEqual(self.gr_ww_7.size(), 7, "Graph with weights should report 7 nodes")
        self.assertIn(0, self.gr_ww_7.get_neighbors(2),
                      "Node 0 should be listed as neighbor of 2 in graph with weights")
        self.assertIn(4, self.gr_ww_7.get_neighbors(2),
                      "Node 4 should be listed as neighbor of 2 in graph with weights")

        self.gr_ww_7.remove_node(2)

        self.assertEqual(self.gr_ww_7.size(), 6, "Graph with weights should report 6 nodes")
        self.assertFalse(self.gr_ww_7.node_exists(2), "Graph with weights should report that node 2 does not exist")
        self.assertNotIn(2, self.gr_ww_7.get_neighbors(0),
                         "Node 2 should NOT be listed as neighbor of 0 in graph with weights")
        self.assertNotIn(2, self.gr_ww_7.get_neighbors(4),
                         "Node 2 should NOT be listed as neighbor of 4 in graph with weights")

    def test_add_and_remove_nodes_by_list(self):
        gr1 = glib.Graph()
        gr2 = glib.Graph(has_weights=True)

        gr1.add_nodes_from_list(['a', 'b', 'c', 'd'])
        self.assertEqual(gr1.size(), 4, "Graph with no weights should report 4 nodes")
        gr1.remove_nodes_from_list(['b', 'd'])
        self.assertEqual(gr1.size(), 2, "Graph with no weights should report 2 nodes")

        gr2.add_nodes_from_list(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'])
        self.assertEqual(gr2.size(), 10, "Graph with weights should report 10 nodes")
        gr2.remove_nodes_from_list(['two', 'four', 'six', 'eight', 'ten'])
        self.assertEqual(gr2.size(), 5, "Graph with weights should report 5 nodes")

    def test_add_and_remove_links_by_list(self):
        gr1 = glib.Graph()

        gr1.add_nodes_from_list(['a', 'b', 'c', 'd'])
        self.assertEqual(gr1.size(), 4, "Graph should report 4 nodes")

        list1 = [('a', 'b'), ('b', 'c'), ('a', 'd'), ('c', 'd')]
        gr1.add_links_from_list(list1)

        self.assertTrue(gr1.are_neighbors('a', 'b'), "Nodes 'a' and 'b' are neighbors")
        self.assertTrue(gr1.are_neighbors('a', 'd'), "Nodes 'a' and 'd' are neighbors")

        list2 = [('a', 'b'), ('a', 'd')]
        gr1.remove_links_from_list_of_neighbors(list2)

        self.assertFalse(gr1.are_neighbors('a', 'b'), "Nodes 'a' and 'b' are not neighbors")
        self.assertFalse(gr1.are_neighbors('a', 'd'), "Nodes 'a' and 'd' are not neighbors")

        gr2 = glib.Graph(has_weights=True)

        gr2.add_nodes_from_list(['a', 'b', 'c', 'd', 'x', 'y'])
        self.assertEqual(gr2.size(), 6, "Graph should report 6 nodes")

        list1 = [('a', 'b', 0.1), ('b', 'c', 0.5), ('a', 'd', 0.7), ('c', 'd', 0.2), ('d', 'x', 0.9)]
        gr2.add_links_from_list(list1)

        self.assertTrue(gr2.are_neighbors('a', 'b'), "Graph should include a link between 'a' and 'b'")
        self.assertTrue(gr2.are_neighbors('a', 'd'), "Graph should include a link between 'a' and 'd'")

        list2 = [('a', 'b'), ('a', 'd'), ('d', 'y'), ('d', 'z')]
        res2 = gr2.remove_links_from_list_of_neighbors(list2)

        self.assertEqual(res2, 2, "Only 2 links can be removed in graph with weights")

        self.assertFalse(gr2.are_neighbors('a', 'b'), "Nodes 'a' and 'b' are not neighbors")
        self.assertFalse(gr2.are_neighbors('a', 'd'), "Nodes 'a' and 'd' are not neighbors")

    def test_add_payload(self):
        gr = glib.Graph()

        gr.add_nodes_from_list([11, 12, 13, 14])
        self.assertEqual(gr.size(), 4, "Graph should report 4 nodes")

        list1 = [(11, 12), (12, 13), (11, 14), (13, 14)]
        gr.add_links_from_list(list1)

        self.assertFalse(gr.has_payload(11), "Graph should report that Node 11 DOES NOT have a payload")

        gr.add_payload(11, {'brand': 'toyota'})
        gr.add_payload(12, {'brand': 'audi'})
        gr.add_payload(13, {'brand': 'ford'})

        self.assertTrue(gr.has_payload(11), "Graph should report that Node 11 has a non-zero payload")

        res1 = gr.get_payload(11)
        res2 = gr.get_payload(12)

        self.assertEqual(res1['brand'], 'toyota', "Node 11 should show a toyota car")
        self.assertEqual(res2['brand'], 'audi', "Node 12 should show an audi car")

        res = self.gr_ww_7.add_payloads_from_list([(4, {'first': 'james', 'last': 'bond'}),
                                                   (5, {'first': 'mike', 'last': 'taylor'}),
                                                   (6, {'first': 'dave', 'last': 'belter'})])

        self.assertEqual(res, 3, "The number of payload additions should be 3")
        self.assertEqual(self.gr_ww_7.get_payload(6)['last'], 'belter', "Returned item should match inoput")

    def test_remove_node_with_payload(self):
        self.assertEqual(self.gr_ww_7.get_payload(3), 103, "Paylod of node 3 should be 103")
        self.gr_ww_7.remove_node(3)
        self.assertFalse(self.gr_ww_7.node_exists(3))

    def test_dfs_traverse(self):
        res = self.gr_ww_7.dfs_traverse(0)
        self.assertEqual(len(res), 7, "DFS result should return all 7 nodes")

        set_nodes = set(self.gr_ww_7.get_nodes())
        set_res = set(res)
        set_diff = set_nodes.difference(set_res)
        self.assertEqual(len(set_diff), 0, "DFS result should contain the same node IDs as the original")

    def test_bfs_traverse(self):
        res = self.gr_ww_7.bfs_traverse(0)
        self.assertEqual(len(res), 7, "BFS result should return all 7 nodes")

        set_nodes = set(self.gr_ww_7.get_nodes())
        set_res = set(res)
        set_diff = set_nodes.difference(set_res)
        self.assertEqual(len(set_diff), 0, "BFS result should contain the same node IDs as the original")

    def test_is_connected_graph(self):
        self.assertTrue(self.gr_ww_7.is_connected_graph(0),
                        "Function should determine that graph is a connected graph")

        self.gr_ww_7.remove_node(6)
        self.assertEqual(self.gr_ww_7.size(), 6, "Graph should have 6 nodes after removal of a node")

        self.gr_ww_7.add_node(9)
        self.assertEqual(self.gr_ww_7.size(), 7, "Graph should have 7 nodes after adding one node")

        self.assertFalse(self.gr_ww_7.is_connected_graph(0),
                         "Function should determine that graph is not a connected graph")

    def test_get_neighbors(self):

        nbor_list = self.gr_ww_7.get_neighbors(5)

        self.assertEqual(len(nbor_list), 3, "Function should report 3 neighbors for node 5")

        self.assertIn(1, nbor_list, "Function should report that node 1 is a neighbor of node 5")
        self.assertIn(4, nbor_list, "Function should report that node 4 is a neighbor of node 5")
        self.assertIn(6, nbor_list, "Function should report that node 6 is a neighbor of node 5")

    def test_get_depth_layer_nodes(self):
        ngr = glib.Graph()

        for k in range(10):
            ngr.add_node(k)

        ngr.add_links_from_list([(0, 1), (0, 2), (0, 3), (1, 6), (1, 5), (2, 4), (5, 6)])
        ngr.add_links_from_list([(3, 4), (6, 7), (5, 8), (4, 8), (4, 9), (9, 8), (4, 5)])

        res0 = ngr.get_depth_layer(node_id=0, layer=0)

        self.assertEqual(len(res0['nodes']), 1, "Layer 0 should have only one node")
        self.assertEqual(res0['nodes'][0], 0, "The only node in layer 0 is the start node, which is node 0")

        res1 = ngr.get_depth_layer(node_id=0, layer=1)
        self.assertEqual(len(res1['nodes']), 3, "Layer 1 should have 3 nodes")

        set1 = {1, 2, 3}
        set2 = set(res1['nodes'])
        num_diff = len(set1.difference(set2))
        self.assertEqual(num_diff, 0, "Layer 1 should have nodes 1, 2, and 3")

        res2 = ngr.get_depth_layer(node_id=0, layer=2)
        self.assertEqual(len(res2['nodes']), 3, "Layer 2 should have 3 nodes")

        set3 = {4, 5, 6}
        set4 = set(res2['nodes'])
        num_diff = len(set3.difference(set4))
        self.assertEqual(num_diff, 0, "Layer 2 should have nodes 4, 5, and 6")

        res10 = ngr.get_depth_layer(node_id=0, layer=10)
        self.assertEqual(res10['layer'], 3, "The maximum non-zero layer in this graph should be 3")

        set5 = {7, 8, 9}
        set6 = set(res10['nodes'])
        num_diff = len(set5.difference(set6))
        self.assertEqual(num_diff, 0, "A request for layer 10 should return layer 3 nodes: 7, 8, 9")

    def test_is_node_in_layer(self):
        ngr = glib.Graph()

        ngr.add_nodes_from_list([k for k in range(10)])
        ngr.add_links_from_list([(0, 1), (0, 2), (0, 3), (1, 6), (1, 5), (2, 4), (5, 6)])
        ngr.add_links_from_list([(3, 4), (6, 7), (5, 8), (4, 8), (4, 9), (9, 8), (4, 5)])

        self.assertTrue(ngr.is_node_in_layer(start_node=0, target_node=0, layer=0), "Node 0 should be in layer 0")
        self.assertTrue(ngr.is_node_in_layer(start_node=0, target_node=3, layer=1), "Node 3 should be in layer 1")
        self.assertTrue(ngr.is_node_in_layer(start_node=0, target_node=5, layer=2), "Node 5 should be in layer 2")

        self.assertFalse(ngr.is_node_in_layer(start_node=0, target_node=8, layer=2), "Node 8 should not be in layer 0")

    def test_shortest_path(self):
        tgr = glib.Graph()

        tgr.add_nodes_from_list([k for k in range(10)])
        tgr.add_links_from_list([(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (2, 5), (3, 5), (3, 7), (4, 6), (5, 6), (6, 7)])
        tgr.add_links_from_list([(4, 8), (6, 8), (6, 9), (8, 9)])

        res0 = tgr.shortest_path(init_id=0, dest_id=0)
        self.assertEqual(len(res0), 1, "Shortest path for a single node should have a length of one")
        self.assertEqual(res0[0], 0, "Shortest path for a single node should have this node as the only element")

        res1 = tgr.shortest_path(0, 1)
        self.assertEqual(len(res1), 2, "Shortest path for node 1 has 2 nodes")

        res2 = tgr.shortest_path(0, 2)
        self.assertEqual(len(res2), 2, "Shortest path for node 2 has 2 nodes")

        res3 = tgr.shortest_path(0, 3)
        self.assertEqual(len(res3), 2, "Shortest path for node 3 has 2 nodes")

        res4 = tgr.shortest_path(0, 4)
        self.assertEqual(len(res4), 3, "Shortest path for node 4 has 3 nodes")

        res5 = tgr.shortest_path(0, 5)
        self.assertEqual(len(res5), 3, "Shortest path for node 5 has 3 nodes")

        res6 = tgr.shortest_path(0, 6)
        self.assertEqual(len(res6), 4, "Shortest path for node 6 has 4 nodes")

        res7 = tgr.shortest_path(0, 7)
        self.assertEqual(len(res7), 3, "Shortest path for node 7 has 3 nodes")

        res8 = tgr.shortest_path(0, 8)
        self.assertEqual(len(res8), 4, "Shortest path for node 8 has 4 nodes")

        res9 = tgr.shortest_path(0, 9)
        self.assertEqual(len(res9), 5, "Shortest path for node 9 has 5 nodes")


if __name__ == '__main__':
    unittest.main()
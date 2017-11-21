#!/usr/bin/python

import networkx as nx
import numpy as np
from argparse import ArgumentParser
import os
from collections import Set


def generate_node_idxs(graph1, graph2):
    dict_ids = {}
    graphs = []
    for graph in [graph1, graph2]:
        gname = os.path.basename(graph)
        gid, ext = os.path.splitext(gname)
        if ext == '.edgelist':
            graphs.append(nx.read_weighted_edgelist(graph))
        elif ext == '.gpickle':
            graphs.append(nx.read_gpickle(graph))
    vertices = []
    for graph in graphs:
        vertices += [int(node) for node in graph.nodes()]
    vertices = sorted(list(set(vertices))) 
    for d3mid, vid in enumerate(vertices):
        dict_ids[d3mid] = vid
    return dict_ids

def save_tgts(dict_ids, fname, graph):
    gname = os.path.basename(graph)
    gid, ext = os.path.splitext(gname)
    with open(fname, "w") as tgtfile:
        tgtfile.write("d3mIndex,graph," + gid + ".nodeID\n")
        for (d3mid, nodeid) in dict_ids.iteritems():
            tgtfile.write(",".join([str(d3mid), gname, str(nodeid)]) + "\n")
    pass

def main():
    parser = ArgumentParser()
    parser.add_argument("graph1", help="the first graph.")
    parser.add_argument("graph2", help="the second graph.")
    parser.add_argument("file1", help="the training file.")
    parser.add_argument("file2", help="the testing file.")
    result = parser.parse_args()
    dict_ids = generate_node_idxs(result.graph1, result.graph2)
    save_tgts(dict_ids, result.file1, result.graph1)
    save_tgts(dict_ids, result.file2, result.graph2)
    return

if __name__ == "__main__":
    main()

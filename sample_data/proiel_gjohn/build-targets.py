#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from collections import defaultdict, namedtuple

target_num = 0

def include(graph, node):
    if node.rel == "pred" or (node.rel == "sub" and len(graph.subtree(node)) > 1):
        return True
    else:
        return False

class Graph:
    def __init__(self, node, deps):
        self.node = node
        self.deps = deps
    
    def roots(self):
        return (self.node[x] for x in graph.deps["-"])
    
    def display(self):
        for root in self.roots():
            self.display_node(root)
    
    def display_node(self, node, indent=0):
        global target_num
        if include(self, node):
            target_num += 1
            print "%06d|%s|%s-%s|%s" % (int(node.ref), node.cv_range, node.rel, node.pos, self.subtree_text(node))
        
        for dep in (self.node[x] for x in self.deps[node.ref]):
            self.display_node(dep, indent + 1)
    
    def subtree(self, node):
        nodes = [node]
        for dep in (self.node[x] for x in self.deps[node.ref]):
            nodes.extend(self.subtree(dep))
        return nodes
    
    def subtree_text(self, node):
        text = " ".join(n.form.replace("+", " ") for n in sorted(self.subtree(node), key=lambda n: n.line_num) if n.pos != "-")
        return text


Node = namedtuple("Node", "line_num book cv_range ref form lemma pos lang parse rel head")

graph = Graph({}, defaultdict(set))


line_num = 0
for line in open(sys.argv[1]):
    if line.strip():
        line_num += 1
        book, cv_range, ref, form, analysis, rel, head = line.strip().split()
        if analysis == "-":
            lemma, pos, lang, parse = "-", "-", "-", "-"
        else:
            lemma, pos, lang, parse = analysis.split(",")
        graph.node[ref] = Node(line_num, book, cv_range, ref, form, lemma, pos, lang, parse, rel, head)
        graph.deps[head].add(ref)
    else:
        graph.display()
        graph = Graph({}, defaultdict(set))

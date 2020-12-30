import enum
import sys

from Utils.color import *


class NodeType(enum.Enum):
    NORMAL = 0
    BLOCK = 1
    SOURCE = 2
    SINK = 3
    VISITED = 4
    PATH = 5


class Node:
    def __init__(self, x: int, y, g=sys.maxsize, h=0):
        self.x = x
        self.y = y
        self.type = NodeType.NORMAL
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.path = []

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        try:
            return self.f == other.f
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.f < other.f
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.f > other.f
        except AttributeError:
            return NotImplemented

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)

    def get_color(self):
        if self.type == NodeType.NORMAL:
            return WHITE
        elif self.type == NodeType.BLOCK:
            return BLACK
        elif self.type == NodeType.SOURCE:
            return ORANGE
        elif self.type == NodeType.SINK:
            return TURQUOISE
        elif self.type == NodeType.VISITED:
            return GREEN
        elif self.type == NodeType.PATH:
            return RED


class NodeQueue:
    def __init__(self):
        self.queue: [Node] = []

    def add(self, node: Node):
        for existing_node in self.queue:
            if existing_node.x == node.x and existing_node.y == node.y:
                existing_node.g = node.g
                existing_node.h = node.h
                existing_node.f = node.f
                self.sort()
                return

        self.queue.append(node)
        self.sort()

    def __repr__(self):
        node_string = ""
        for node in self.queue:
            node_string += f"{str(node)}\n"

        return node_string

    def sort(self):
        self.queue.sort()

    def is_empty(self):
        return len(self.queue) == 0

    def pop(self):
        return self.queue.pop(0)


if __name__ == '__main__':
    nq = NodeQueue()
    n5 = Node(5, 5, g=5, h=5)
    n3 = Node(3, 3, g=3, h=3)
    n2 = Node(2, 2, g=2, h=2)
    n1 = Node(1, 1, g=1, h=1)

    nq.add(n5)
    nq.add(n3)
    nq.add(n2)
    nq.add(n1)

    n5.f = 0

    nq.sort()

    print("")

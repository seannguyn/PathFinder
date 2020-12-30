from __future__ import annotations

import time

import pygame

from Utils.node import Node, NodeType, NodeQueue


class Grid:
    def __init__(self, size: int):
        self.size = size
        self.nodes = self.initialize_nodes()
        self.path = []
        self.source = None
        self.sink = None

    def initialize_nodes(self) -> [[Node]]:
        grid_nodes = []
        for y in range(0, self.size):
            horizontal_nodes = []
            for x in range(0, self.size):
                horizontal_nodes.append(Node(x, y))
            grid_nodes.append(horizontal_nodes)

        return grid_nodes

    def get_neighbor(self, current_node: Node) -> [Node]:
        direction = [-1, 0, 1]
        neighbors = []

        for x_direction in direction:
            for y_direction in direction:
                if x_direction == 0 and y_direction == 0: # \
                        # or x_direction != 0 and y_direction != 0:
                    continue

                x_new = current_node.x + x_direction
                y_new = current_node.y + y_direction

                if self.is_in_grid(x_new, y_new) and not self.is_blocked(x_new, y_new):
                    neighbors.append(self.nodes[y_new][x_new])

        return neighbors

    def is_in_grid(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def is_blocked(self, x: int, y: int) -> bool:
        # convert cartesian coordinates to str len
        return self.nodes[y][x].type == NodeType.BLOCK

    def get_node_shape(self, x: int, y: int, block_size: int):
        rect = pygame.Rect(x * block_size, y * block_size,
                           block_size, block_size)
        color = self.nodes[y][x].get_color()

        return rect, color

    def make_block(self, x: int, y: int):
        if self.nodes[y][x].type == NodeType.NORMAL:
            self.nodes[y][x].type = NodeType.BLOCK
            return True
        return False

    def make_source(self, x: int, y: int):
        if self.nodes[y][x].type == NodeType.NORMAL:
            self.nodes[y][x].type = NodeType.SOURCE
            self.source = self.nodes[y][x]
            return True
        return False

    def make_sink(self, x: int, y: int):
        if self.nodes[y][x].type == NodeType.NORMAL:
            self.nodes[y][x].type = NodeType.SINK
            self.sink = self.nodes[y][x]
            return True
        return False

    def make_normal(self, x: int, y: int):
        self.nodes[y][x].type = NodeType.NORMAL

    def make_visited(self, x: int, y: int):
        if self.nodes[y][x].type == NodeType.NORMAL:
            self.nodes[y][x].type = NodeType.VISITED

    def make_path(self):
        for node in self.sink.path:
            if node.type != NodeType.SINK and node.type != NodeType.SOURCE:
                node.type = NodeType.PATH

    def a_star(self, draw):

        visited = []

        node_queue = NodeQueue()

        # reset source
        self.source.g = 0
        self.source.h = 0
        self.source.f = 0
        self.source.path = [self.source]

        # add source to the queue
        node_queue.add(self.source)

        while not node_queue.is_empty():
            current_node = node_queue.pop()

            visited.append(current_node)
            self.make_visited(current_node.x, current_node.y)

            if current_node.x == self.sink.x and current_node.y == self.sink.y:
                self.make_path()
                draw()
                break

            neighbors = self.get_neighbor(current_node)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue

                neighbor.g = current_node.g + 1
                neighbor.h = self.heuristic(neighbor)
                neighbor.f = neighbor.g + neighbor.h

                neighbor.path = current_node.path + [neighbor]

                node_queue.add(neighbor)

            draw()

    def dijkstra(self, draw):
        visited = []

        node_queue = NodeQueue()

        # reset source
        self.source.g = 0
        self.source.h = 0
        self.source.f = 0
        self.source.path = [self.source]

        # add source to the queue
        node_queue.add(self.source)

        while not node_queue.is_empty():
            current_node = node_queue.pop()

            visited.append(current_node)
            self.make_visited(current_node.x, current_node.y)

            if current_node.x == self.sink.x and current_node.y == self.sink.y:
                self.make_path()
                draw()
                break

            neighbors = self.get_neighbor(current_node)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue

                neighbor.g = current_node.g + 1
                neighbor.h = 0
                neighbor.f = neighbor.g + neighbor.h

                neighbor.path = current_node.path + [neighbor]

                node_queue.add(neighbor)

            draw()

    def __repr__(self):
        grid_representation = ""
        for y in range(0, self.size):
            for x in range(0, self.size):
                grid_representation += " " + str(self.nodes[y][x])
            grid_representation += "\n"

        return grid_representation

    def heuristic(self, current_node) -> int:
        return abs(self.sink.x - current_node.x) + abs(self.sink.y - current_node.y)


if __name__ == '__main__':
    grid = Grid(9)

    grid.source = grid.nodes[0][0]

    grid.sink = grid.nodes[5][5]

    grid.a_star()

    print("yo")

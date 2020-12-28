from __future__ import annotations
import pygame
import sys
from Utils.color import *
from Utils.grid import Grid


WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
BLOCK_SIZE = 20
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Path Finding Algorithm")
GRID = Grid(40)
SOURCE = False
SINK = False
ACTIVE = False


def draw_grid(grid: Grid, screen, window_width, window_height, block_size):

    # Draw node
    for y in range(grid.size):
        for x in range(grid.size):
            rect, color = grid.get_node_shape(x, y, block_size)
            pygame.draw.rect(screen, color, rect)

    # Draw line grid
    for y in range(grid.size):
        pygame.draw.line(screen, GREY, (0, y * block_size), (window_width, y * block_size))
    for x in range(grid.size):
        pygame.draw.line(screen, GREY, (x * block_size, 0), (x * block_size, window_height))

    pygame.display.update()


if __name__ == '__main__':

    def decide_node_type(mouse_position: (int, int)):
        global SOURCE
        global SINK
        global ACTIVE
        global BLOCK_SIZE
        global GRID

        x_index = mouse_position[0] // BLOCK_SIZE
        y_index = (mouse_position[1]) // BLOCK_SIZE
        if not SOURCE:
            SOURCE = GRID.make_source(x_index, y_index)
        elif not SINK:
            SINK = GRID.make_sink(x_index, y_index)
        else:
            GRID.make_block(x_index, y_index)

    while True:
        SCREEN.fill(WHITE)
        draw_grid(GRID, SCREEN, WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # LEFT
                    pos = pygame.mouse.get_pos()
                    decide_node_type(pos)
                    ACTIVE = True

                if event.button == 2:  # MIDDLE
                    pass

                if event.button == 3:  # RIGHT
                    pass

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # LEFT
                    ACTIVE = False

            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if ACTIVE:
                    decide_node_type(pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and SOURCE and SINK:
                    GRID.a_star(lambda: draw_grid(GRID, SCREEN, WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE))
                if event.key == pygame.K_d and SOURCE and SINK:
                    GRID.dijkstra(lambda: draw_grid(GRID, SCREEN, WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE))
                elif event.key == pygame.K_c:
                    SOURCE = False
                    SINK = False
                    GRID = Grid(40)

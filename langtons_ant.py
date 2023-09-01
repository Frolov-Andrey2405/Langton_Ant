import copy
import random
import sys
import time
import bext


class LangtonsAntSimulation:
    def __init__(self):
        self.WIDTH, self.HEIGHT = bext.size()
        self.WIDTH -= 1
        self.HEIGHT -= 1  # (!) Try changing this to 1 or 50.
        self.NUMBER_OF_ANTS = 10  # (!) Try changing this to 1 or 50.
        self.PAUSE_AMOUNT = 0.1  # (!) Try changing this to 1.0 or 0.0.

        self.ANT_UP = '^'
        self.ANT_DOWN = 'v'
        self.ANT_LEFT = '<'
        self.ANT_RIGHT = '>'

        self.ANT_COLOR = 'red'
        self.BLACK_TILE = 'black'
        self.WHITE_TILE = 'white'

        self.NORTH = 'north'
        self.SOUTH = 'south'
        self.EAST = 'east'
        self.WEST = 'west'

        self.board = {'width': self.WIDTH, 'height': self.HEIGHT}
        self.ants = []

    def initialize(self):
        bext.fg(self.ANT_COLOR)
        bext.bg(self.WHITE_TILE)
        bext.clear()
        self.create_ants()

    def create_ants(self):
        for _ in range(self.NUMBER_OF_ANTS):
            ant = {
                'x': random.randint(0, self.WIDTH - 1),
                'y': random.randint(0, self.HEIGHT - 1),
                'direction': random.choice([self.NORTH, self.SOUTH, self.EAST, self.WEST]),
            }
            self.ants.append(ant)

    def main(self):
        self.initialize()
        changed_tiles = []

        while True:
            self.display_board(changed_tiles)
            changed_tiles = []

            next_board = copy.copy(self.board)

            for ant in self.ants:
                if self.board.get((ant['x'], ant['y']), False) == True:
                    next_board[(ant['x'], ant['y'])] = False
                    ant['direction'] = self.turn_clockwise(ant['direction'])
                else:
                    next_board[(ant['x'], ant['y'])] = True
                    ant['direction'] = self.turn_counter_clockwise(
                        ant['direction'])
                changed_tiles.append((ant['x'], ant['y']))

                ant['x'], ant['y'] = self.move_ant(
                    ant['x'], ant['y'], ant['direction'])
                changed_tiles.append((ant['x'], ant['y']))

            self.board = next_board

    def turn_clockwise(self, direction):
        clockwise_turn = {
            self.NORTH: self.EAST,
            self.EAST: self.SOUTH,
            self.SOUTH: self.WEST,
            self.WEST: self.NORTH
        }
        return clockwise_turn[direction]

    def turn_counter_clockwise(self, direction):
        counter_clockwise_turn = {
            self.NORTH: self.WEST,
            self.WEST: self.SOUTH,
            self.SOUTH: self.EAST,
            self.EAST: self.NORTH
        }
        return counter_clockwise_turn[direction]

    def move_ant(self, x, y, direction):
        if direction == self.NORTH:
            y -= 1
        elif direction == self.SOUTH:
            y += 1
        elif direction == self.WEST:
            x -= 1
        elif direction == self.EAST:
            x += 1

        x %= self.WIDTH
        y %= self.HEIGHT
        return x, y

    def display_board(self, changed_tiles):
        for x, y in changed_tiles:
            bext.goto(x, y)
            if self.board.get((x, y), False):
                bext.bg(self.BLACK_TILE)
            else:
                bext.bg(self.WHITE_TILE)

            ant_is_here = False
            for ant in self.ants:
                if (x, y) == (ant['x'], ant['y']):
                    ant_is_here = True
                    print(self.get_ant_symbol(ant['direction']), end='')
                    break
            if not ant_is_here:
                print(' ', end='')

        bext.goto(0, self.HEIGHT)
        bext.bg(self.WHITE_TILE)
        print('Press Ctrl-C to quit.', end='')

        sys.stdout.flush()
        time.sleep(self.PAUSE_AMOUNT)

    def get_ant_symbol(self, direction):
        symbols = {
            self.NORTH: self.ANT_UP,
            self.SOUTH: self.ANT_DOWN,
            self.EAST: self.ANT_LEFT,
            self.WEST: self.ANT_RIGHT
        }
        return symbols[direction]


if __name__ == '__main__':
    try:
        simulation = LangtonsAntSimulation()
        simulation.main()
    except KeyboardInterrupt:
        print("Langton's Ant Simulation")
        sys.exit()

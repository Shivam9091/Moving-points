import random
import time
import os

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other): 
        return Point(self.x + other.x, self.y + other.y)


class Grid:
    directions = {'north': Point(0, -1), 'south': Point(0, 1), 'east': Point(1, 0), 'west': Point(-1, 0), 'north_east': Point(1, -1), 'north_west': Point(-1, -1), 'south_east': Point(1, 1), 'south_west': Point(-1, 1),}

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.generate_grid()

    def generate_grid(self):
        grid = []
        for _ in range(self.height):
            width = []
            for _ in range(self.width):
                width.append(None)
            grid.append(width)
        return grid

    def set_point(self, point, value):
        self.grid[point.y][point.x] = value

    def get_point(self, point):
        return self.grid[point.y][point.x]

    def is_within(self, point):
        try:
            self.grid[point.y][point.x]
            return True
        except IndexError:
            return False
        
    def display(self):
        for i in self.grid:
            print(i)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.grid):
            value = self.grid[self.n]
            self.n += 1
            return value
        else:
            raise StopIteration

class Entity:
    def __init__(self, string, *args, **kwargs):
        self.string = string
        self.is_able = False


class Wall(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BouncingEntity(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.random_direction = random.choice(list(Grid.directions.keys()))
        self.is_able = True

    def act(self, view):
        if view.look(self.random_direction) != ' ':
            self.random_direction = view.find(' ')
            if self.random_direction is None:
                self.random_direction = random.choice(list(Grid.directions.keys()))
        return {'type': 'move', 'direction': self.random_direction}


class World:
    def __init__(self, list_, dict_):
        self.list_ = list_
        self.dict_ = dict_
        self.world = Grid(len(list_[0]), len(list_))
        self.set_symbol()

    def set_symbol(self):
        for y, line in enumerate(self.list_):
            for x in range(0, len(line)):
                self.world.set_point(Point(x,y), self.set_type(self.dict_, line[x]))

    def set_type(self, legend, leg_str):
        if leg_str == ' ':
            return None
        else:
            return legend[leg_str](leg_str)

    def get_char(self, elem):
        if elem == None:
            return ' '
        else:
            return elem.string

    def check_destination(self, action, point):
        if action['direction'] in Grid.directions:
            new_point = point + Grid.directions[action['direction']]
            if self.world.is_within(new_point):
                return new_point

    def let_act(self, entity, point):
        action = entity.act(View(self, point))
        if action['type'] == 'move':
            self.world.set_point(self.check_destination(action, point), entity)
            self.world.set_point(point, None)

    def turn(self):
        moved_this_turn = []
        for y, line in enumerate(self.world):
            for x in range(0, len(line)):
                point = Point(x,y)
                get_point = self.world.get_point(point)
                if isinstance(get_point, Entity):
                    if get_point.is_able and get_point not in moved_this_turn:
                        self.let_act(get_point, point)
                        moved_this_turn.append(get_point)

    def display(self):
        output = ''
        for i in self.world:
            for j in i:
                output += self.get_char(j)
            output += '\n'
        return output

    def __getitem__(self, key):
        return self.list_[key]



class View:
    def __init__(self, world, point):
        self.world = world
        self.point = point

    def look(self, direction):
        given_point = self.point + Grid.directions[direction]
        if self.world.world.is_within(given_point):
            return self.world.get_char(self.world.world.get_point(given_point))
        else:
            return "#"

    def find_all(self, symbol):
        symbol_is_there = []
        for i in self.world.world.directions:
            if self.look(i) == symbol:
                symbol_is_there.append(i)
        return symbol_is_there
                
    def find(self, symbol):
        found_by_symbol = self.find_all(symbol)
        if len(found_by_symbol) == 0:
            return None
        else:
            return random.choice(found_by_symbol)


plan = ["############################",
        "#      #   #         x    ##",
        "#                      x   #",
        "#     x   #####            #",
        "##        # x #    ##      #",
        "###          ##     #      #",
        "#          ###      #      #",
        "#   ####    x              #",
        "#   ##              x      #",
        "#    #   x       x     ### #",
        "#    #                     #",
        "############################"]

world = World(plan, {"#": Wall, 'x': BouncingEntity })

while True:
    os.system('cls')
    print(world.display())
    world.turn()
    time.sleep(0.07)


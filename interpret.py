import sys
import math
import fileinput

class Shape:
    def __init__(self, grid, row, col, visited):
        # the symbol of the shape
        self.symbol = grid[row][col]

        # Breadth first traversal
        next = []
        next.append((row, col))
        visited.append((row, col))
        base = 0
        while len(next) > base:
            y = next[base][0]
            x = next[base][1]
            # add neighbours
            l = [0, 1, 0, -1]
            for i in range(4):
                next_y = y + l[i]
                if not (0 <= next_y < len(grid)):
                    continue
                next_x = x + l[(i + 1) % 4]
                if not (0 <= next_x < len(grid[next_y])):
                    continue
                if grid[next_y][next_x] == self.symbol and (next_y, next_x) not in visited:
                    next.append((next_y, next_x))
                    visited.append((next_y, next_x))
            base += 1
        self.count = base

        # normalise
        next.sort()
        self.positions = next
        min_y = min(next, key=lambda pos: pos[0])[0]
        min_x = min(next, key=lambda pos: pos[1])[1]
        max_x = max(next, key=lambda pos: pos[1])[1]
        self.y = min_y
        self.x = min_x
        self.width = max_x - min_x + 1

    def ordering(self):
        # assume positions is sorted
        max_y = self.positions[-1][0]
        # order by number of tiles,
        # lowest position,
        # count of tiles at that height
        return (self.count, max_y, [y for y, x in self.positions].count(max_y))

    def print(self):
        y, x = self.y, self.x
        for pos in self.positions:
            while y < pos[0]:
                print()
                x = self.x
                y += 1
            while x < pos[1]:
                print(' ', end='')
                x += 1
            print(self.symbol, end='')
            x += 1
        print()

    def to_image(self):
        image = []
        x, y = 0, 0
        for pos in self.positions:
            while y < pos[0]:
                image.append([])
                x = 0
                y += 1
            while x < pos[1]:
                image[-1].append(' ')
                x += 1
            x += 1
        return image


def find_real(stiles):
    real_tiles = set()
    for real in stiles:
        y, x, symbol = real
        if (y + 1, x - 1, symbol) in stiles and (y + 1, x + 1, symbol) in stiles and (y + 2, x, symbol) in stiles:
            real_tiles.add(real)
            real_tiles.add((y + 1, x - 1, symbol))
            real_tiles.add((y + 1, x + 1, symbol))
            real_tiles.add((y + 2, x    , symbol))
    real_tiles = list(real_tiles)
    real_tiles.sort()
    return real_tiles


def parse_shapes(grid):
    shapes = []
    visited = []
    for row, line in enumerate(grid):
        for col, symbol in enumerate(line):
            if not symbol.isspace() and (row, col) not in visited:
                shapes.append(Shape(grid, row, col, visited))
    return shapes


# assume ordered
def calculate_offsets(shapes):
    acc = 0
    for shape in shapes:
        shape.buffer_x_offset = acc
        acc += shape.width


def sparse_to_image(tiles):
    w_index = 0
    h_index = 0
    result = [[]]
    for tile in tiles:
        while tile[0] > h_index:
            w_index = 0
            h_index += 1
            result.append([])
        while tile[1] > w_index:
            result[h_index].append(" ")
            w_index += 1
        result[h_index].append(tile[2])
        w_index += 1
    return ["".join(line) for line in result]


def make_sorted_shapes_image(shapes):
    buffer = shapes_to_sparse_list(shapes)
    return sparse_to_image(buffer)


def shapes_to_sparse_list(shapes):
    buffer = [(tile[0], tile[1] - shape.x + shape.buffer_x_offset, shape.symbol) for shape in shapes for tile in shape.positions]
    buffer.sort()
    return buffer


def make_rectangle(shapes, width):
    buffer = shapes_to_sparse_list(shapes)
    real = find_real(buffer)

    # start building the final rectangle
    # add the real symbols
    final_rect = [tile[2] for tile in real]
    # add the imaginary symbols
    final_rect += [tile[2] for tile in buffer if tile not in real]

    # run the copy rule
    for i in range(max(0, width + 1 - len(real)), width + 1):
        if (len(real) + i) % width == 0:
            continue
        final_rect.append(final_rect[len(real) + i])

    # reformat
    formatted_rect = []
    for i in range(math.ceil(len(final_rect) / width)):
        formatted_rect.append("".join(final_rect[i * width:min((i + 1) * width, len(final_rect))]))
    return formatted_rect


def interpret_rectangle(grid):
    # The width includes whitespace
    width = max([len(l) for l in grid])

    shapes = parse_shapes(grid)
    shapes.sort(key=lambda shape: shape.ordering(), reverse=True)
    calculate_offsets(shapes)

    return make_rectangle(shapes, width), width


def debug_interpret_rectangle(grid):
    width = max([len(l) for l in grid])

    shapes = parse_shapes(grid)
    shapes.sort(key=lambda shape: shape.ordering(), reverse=True)
    calculate_offsets(shapes)
    sorted_shapes_image = make_sorted_shapes_image(shapes)

    buffer = shapes_to_sparse_list(shapes)
    real = find_real(buffer)
    real = [(i // width, i % width, tile[2]) for i, tile in enumerate(real)]
    real_image = sparse_to_image(real)

    return width, sorted_shapes_image, real_image, make_rectangle(shapes, width)

def interpret():
    # read the input and clean up newlines
    with fileinput.input() as f:
        content = [line for line in f]
    content = [[char for char in list(line) if char != '\n'] for line in content]

    next_rect, width = interpret_rectangle(content)
    for line in next_rect:
        print(line)
    print()
    while len(next_rect[-1]) == width:
        next_rect, width = interpret_rectangle(next_rect)
        for line in next_rect:
            print(line)
        print()

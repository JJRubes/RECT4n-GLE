import sys

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
        max_x = max(next, key=lambda pos: pos[0])[0]
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


def find_real(stiles, symbol):
    # split into real and imaginary
    real_below = lambda rp: (
            (rp[0] + 1, rp[1] - 1, symbol) in stiles and
            (rp[0] + 1, rp[1] + 1, symbol) in stiles and
            (rp[0] + 2, rp[1]    , symbol) in stiles
            )
    return [real for real in stiles if real_below(real)]


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


def make_rectangle(shapes, width):
    # put it all into a list
    buffer = [(tile[0], tile[1] - shape.x + shape.buffer_x_offset, shape.symbol) for shape in shapes for tile in shape.positions]
    real = []
    symbols = {shape.symbol for shape in shapes}
    for symbol in symbols:
        only_one_symbol = [tile for tile in buffer if tile[2] == symbol]
        real += find_real(only_one_symbol, symbol)
    real.sort(reverse=True) # <- is this the correct ordering?

    # start building the final rectangle
    # add the real symbols
    final_rect = [tile[2] for tile in real]
    # add the imaginary symbols
    final_rect += [tile[2] for tile in buffer if tile not in real]

    # run the copy rule
    copy_rule = [final_rect[x + width + 1] for x in range(len(real)) if x + width + 1 < len(final_rect)]
    final_rect += copy_rule
    return final_rect


def one_iteration(grid):
    # The width includes whitespace
    width = max([len(l) for l in grid])

    shapes = parse_shapes(grid)

    shapes.sort(key=lambda shape: shape.ordering(), reverse=True)
    print("Shapes:")
    for shape in shapes:
        shape.print()

    calculate_offsets(shapes)

    return make_rectangle(shapes, width), width


def interpret(file):
    # read the input and clean up newlines
    with open(file, 'r') as f:
        content = f.readlines()
    content = [[c for c in list(s) if c != '\n'] for s in content]
    print("input file:")
    for line in content:
        print("  " + "".join(line))

    final_rect, width = one_iteration(content)

    if len(final_rect) % width == 0:
        print("continue")
    else:
        print("halt")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit()
    interpret(sys.argv[1])

import sys

# additional things to ask:
# - how is the program's width calculated
#   It includes whitespace (not newlines)
# - how do you break size ties
#   look at the bottom row
# - which order to add real symbols
# - do real symbols depend on other shapes
#   e.g.  AA
#         A A
#          AA
#   this is 2 shapes, are there still real symbols here?

class Shape:
    def __init__(self, contents, row, col, visited):
        # the symbol of the shape
        self.symbol = contents[row][col]

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
                if not (0 <= next_y < len(contents)):
                    continue
                next_x = x + l[(i + 1) % 4]
                if not (0 <= next_x < len(contents[next_y])):
                    continue
                if contents[next_y][next_x] == self.symbol and (next_y, next_x) not in visited:
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
        self.offset = (min_y, min_x)
        self.width = max_x - min_x + 1

    def ordering(self):
        # assume positions is sorted
        max_y = self.positions[-1][0]
        # order by number of tiles
        # lowest position
        # count of tiles at that position
        return (self.count, max_y, [y for y, x in self.positions].count(max_y))

    def print(self):
        y, x = self.offset
        for pos in self.positions:
            while y < pos[0]:
                print()
                x = self.offset[1]
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


def interpret(file):
    # read the input and clean up newlines
    with open(file, 'r') as f:
        content = f.readlines()
    content = [[c for c in list(s) if c != '\n'] for s in content]
    print("input file:")
    for line in content:
        print("  " + "".join(line))

    # The width includes whitespace
    width = max([len(l) for l in content])

    # parse the shapes
    shapes = []
    visited = []
    symbols = set()
    for row, line in enumerate(content):
        for col, symbol in enumerate(line):
            if not symbol.isspace() and (row, col) not in visited:
                shapes.append(Shape(content, row, col, visited))
                symbols.add(symbol)

    # doing tie breaking by what was parsed first
    # i.e. left to right, top to bottom
    shapes.sort(key=lambda shape: shape.ordering(), reverse=True)
    print("Shapes:")
    for shape in shapes:
        shape.print()

    # find the buffer offsets
    # and add them to symbol list
    same_symbol = {}
    acc = 0
    for shape in shapes:
        shape.buffer_offset = acc
        if shape.symbol not in same_symbol:
            same_symbol[shape.symbol] = []
        same_symbol[shape.symbol].append(shape)
        acc += shape.width

    # put it all into a list
    buffer = [(tile[0] - shape.offset[0], tile[0] - shape.offset[1] + shape.buffer_offset, shape.symbol) for shape in shapes for tile in shape.positions]
    real = []
    for symbol in symbols:
        only_one_symbol = [tile for tile in buffer if tile[2] == symbol]
        real += find_real(only_one_symbol, symbol)
    real.sort(reverse=True)

    # start building the final rectangle
    final_rect = [tile[2] for tile in real]
    final_rect += [tile[2] for tile in buffer if tile not in real]

    # do the final thingo
    bonus = [final_rect[x + width + 1] for x in range(len(real)) if x + width + 1 < len(final_rect)]

    final_rect += bonus

    if len(final_rect) % width == 0:
        pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit()
    interpret(sys.argv[1])

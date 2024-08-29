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
    def __init__(self, contents, row, col):
        self.symbol = contents[row][col]
        next = []
        next.append((row, col))
        base = 0
        while len(next) > base:
            y = next[base][0]
            x = next[base][1]

            # clear it
            contents[y][x] = ' '

            # add neighbours
            l = [0, 1, 0, -1]
            for i in range(4):
                next_y = y + l[i]
                if not (0 <= next_y < len(contents)):
                    continue
                next_x = x + l[(i + 1) % 4]
                if not (0 <= next_x < len(contents[next_y])):
                    continue
                if contents[next_y][next_x] == self.symbol:
                    next.append((next_y, next_x))

            base += 1
        self.count = base

        # normalise
        next.sort()
        min_y = min(next, key=lambda pos: pos[0])[0]
        min_x = min(next, key=lambda pos: pos[1])[1]
        self.positions = [(pos[0] - min_y, pos[1] - min_x) for pos in next]
        self.offset = (min_y, min_x)

        # split into real and imaginary
        real_below = lambda rp: (
                (rp[0] + 1, rp[1] - 1) in self.positions and
                (rp[0] + 1, rp[1] + 1) in self.positions and
                (rp[0] + 2, rp[1]    ) in self.positions
                )
        self.real = [real_pos for real_pos in self.positions if real_below(real_pos)]
        self.imaginary = [im_pos for im_pos in self.positions if im_pos not in self.real]

    def print(self):
        x, y = 0, 0
        for pos in self.positions:
            while y < pos[0]:
                print()
                x = 0
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


def interpret(file):
    with open(file, 'r') as f:
        content = f.readlines()
    content = [list(s) for s in content]
    print("input file:")
    for line in content:
        print("  " + "".join(line), end='')

    # parse the shapes
    shapes = []
    for row, line in enumerate(content):
        for col, symbol in enumerate(line):
            if not symbol.isspace():
                shapes.append(Shape(content, row, col))
    # doing tie breaking by what was parsed first
    # i.e. left to right, top to bottom
    shapes.sort(lambda shape: shape.count)
    for shape in shapes:
        shape.print()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit()
    interpret(sys.argv[1])

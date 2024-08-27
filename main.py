import sys

# additional things to ask:
# - how is the program's width calculated
# - how do you break size ties

# start in the top right
# if there is a non-space start a new shape
#   bfs to add all the elements to the shape

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

    shapes = []
    for row, line in enumerate(content):
        for col, symbol in enumerate(line):
            if not symbol.isspace():
                shapes.append(Shape(content, row, col))
    for shape in shapes:
        shape.print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit()
    interpret(sys.argv[1])

from interpret import *

test_folder = "./test/"
test_cases = [
        "example",
        "interesting_sort",
        "simple_halt",
        "sorted_real",
        "copy_edge_case",
        ]


def make_grid(section):
    return [list(line) for line in section.splitlines()]


def compare(given, expected):
    if len(given) != len(expected):
        return False
    for i, val in enumerate(given):
        if expected[i] != val:
            return False
    return True

def print_error(test, expected, actual, file):
    print(f"Error in {file}:")
    print(test)
    print("Expected:")
    for line in expected:
        print(f"  {line}")
    print("Actual:")
    for line in actual:
        print(f"  {line}")

def test_steps(test_case):
    sections = None
    with open(test_folder + test_case + ".txt") as f:
        test_info = f.read()
        sections = test_info.split("===\n")
    width, shape_image, real_image, result = debug_interpret_rectangle(make_grid(sections[0]))
    expected_shapes = sections[1].splitlines()
    if not compare(shape_image, expected_shapes):
        print_error(sections[0], expected_shapes, shape_image, test_case)
        return
    expected_real = sections[2].splitlines()
    if not compare(real_image, expected_real):
        print_error(sections[0], expected_real, real_image, test_case)
        return
    expected = sections[-1].splitlines()
    if not compare(result, expected):
        print_error(sections[0], expected, result, test_case)


if __name__ == "__main__":
    for test_case in test_cases:
        test_steps(test_case)

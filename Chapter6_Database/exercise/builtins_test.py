import builtins


def print_test():
    print(__builtins__ is builtins)
    print(__builtins__ is builtins.__dict__)
    print(type(__builtins__))


if __name__ == "__main__":
    print_test()

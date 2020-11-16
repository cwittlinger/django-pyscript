
def do_something(number: int, a: int, b: str, c: float = 3.2):
    print(a, b, c)


_CALLABLE = do_something


def do_something_else(task):
    print(task)
    print("HERE")

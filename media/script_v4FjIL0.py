def run(number: int, text: str = "hello", floating_number: float = 10.2):
    print(number, type(number))
    print(text, type(text))
    print(floating_number, type(floating_number))


_CALLABLE = run
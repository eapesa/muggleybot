import random
import string

def generate(size=6):
    # NOTE: // ==> integer division
    letter_length = size // 2
    number_length = size - letter_length

    letter_chars = string.ascii_uppercase
    letters = "".join(random.choice(letter_chars) for i in range(letter_length))

    number_chars = string.digits
    numbers = "".join(random.choice(number_chars) for i in range(number_length))

    return letters + numbers

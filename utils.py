import random


def camel_to_snake(name):
    """Convert CamelCase to snake_case."""
    snake_case = ""
    for i, char in enumerate(name):
        if char.isupper() and i != 0:
            snake_case += "_"
        snake_case += char.lower()
    return snake_case


def pick_random_key_value(data: dict):
    # Pick a random key-value pair
    random_key, random_value = random.choice(list(data.items()))
    return [random_key, random_value]

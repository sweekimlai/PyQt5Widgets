import sys


def greet(who):
    fruits = ["apple", "banana", "orange", "melon", "pineapple", "pearl"]
    for f in fruits:
        print("{0} is eating {1}".format(who, f))

    greeting = "Hello {}".format(who)
    return greeting


print(greet("Batman"))

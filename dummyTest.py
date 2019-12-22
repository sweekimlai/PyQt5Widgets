import sys

from PyQt5 import QtCore, QtGui

print(sys.version)
print(sys.executable)


def greet(who):
    greeting = "Hello {}".format(who)
    return greeting


print(greet("Whoever lah"))

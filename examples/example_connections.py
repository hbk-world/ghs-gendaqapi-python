import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src import ghsapi


def main():

    Gen7i = ghsapi.GHS()

    returnVar = Gen7i.GHSConnect("localhost", 8006)
    print("GHSConnect ", returnVar)

    returnVar = Gen7i.GHSDisconnect()
    print("GHSDisconnect ", returnVar)


if __name__ == "__main__":
    main()

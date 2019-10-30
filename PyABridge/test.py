
import sys
from PyABridge import ABridge


def onData(data):
    return data


def main():
    ab = ABridge.ABridge()
    ab.setDataCallback(onData)

    ab.start()


if __name__ == "__main__":
    main()

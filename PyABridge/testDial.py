
import sys
from ABridge import ABridge


def onData(data):
    return data


def main():
    ab = ABridge()
    ab.setDataCallback(onData)

    ab.start()


if __name__ == "__main__":
    main()

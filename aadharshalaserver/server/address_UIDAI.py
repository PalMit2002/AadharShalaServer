import string
import argparse

'''
parser = argparse.ArgumentParser()
parser.add_argument('--address', type=str, required=True)
args = parser.parse_args()
'''

address = "something,something"


def new_address(address):
    ad = address.split(",")

    for i in range(len(ad)):
        if ad.count(ad[i]) > 1:
            ad[i] = "xxxxx"

    try:
        ad.remove("xxxxx")
    except:
        pass

    new_ad = ""
    for i in ad:
        new_ad += i + ","

    return new_ad[:-1].title()


if __name__ == "__main__":
    print(new_address(address))

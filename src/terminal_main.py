
from src.faceoff_data import HUSKIES, ZONE_MAPPING

if __name__ == '__main__':
    # ask for opponents centers
    ops = input("Add opponents centers #'s followed by a space:\n")
    ops_nums = ops.split(" ")

    # add opps centers #s into our vs for each of our guys
    for key in HUSKIES:
        for num in ops_nums:
            HUSKIES[key]["vs"][num] = {"w": 0, "l": 0}

    # faceoff time
    zone = input("What zone (1-9)?\n")
    husky = input("What Husky?\n")
    other_guy = input("What opp center?\n")
    result = input("Result (W/L)?\n")

    # adding stats
    # TODO: Add try block
    HUSKIES[husky]["vs"][other_guy][result] += 1
    mapped_zone = ZONE_MAPPING[zone]
    HUSKIES[husky]["zone"][mapped_zone][result] += 1


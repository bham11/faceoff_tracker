HUSKIES = {
    "27": {
        "vs": {

        },
        "zone": {
            "LD": {"w": 0, "l": 0},
            "RD": {"w": 0, "l": 0},
            "RO": {"w": 0, "l": 0},
            "LO": {"w": 0, "l": 0},
            "C": {"w": 0, "l": 0},
            "LDNZ": {"w": 0, "l": 0},
            "RDNZ": {"w": 0, "l": 0},
            "LONZ": {"w": 0, "l": 0},
            "RONZ": {"w": 0, "l": 0},
        }
    },
    "29": {
        "vs": {

        },
        "zone": {
            "LD": {"w": 0, "l": 0},
            "RD": {"w": 0, "l": 0},
            "RO": {"w": 0, "l": 0},
            "LO": {"w": 0, "l": 0},
            "C": {"w": 0, "l": 0},
            "LDNZ": {"w": 0, "l": 0},
            "RDNZ": {"w": 0, "l": 0},
            "LONZ": {"w": 0, "l": 0},
            "RONZ": {"w": 0, "l": 0},
        }
    },
    "10": {
        "vs": {

        },
        "zone": {
            "LD": {"w": 0, "l": 0},
            "RD": {"w": 0, "l": 0},
            "RO": {"w": 0, "l": 0},
            "LO": {"w": 0, "l": 0},
            "C": {"w": 0, "l": 0},
            "LDNZ": {"w": 0, "l": 0},
            "RDNZ": {"w": 0, "l": 0},
            "LONZ": {"w": 0, "l": 0},
            "RONZ": {"w": 0, "l": 0},
        }
    }
}

ZONE_MAPPING = {
    "1": "LD",
    "2": "RD",
    "3": "RO",
    "4": "LO",
    "5": "C",
    "6": "LDNZ",
    "7": "RDNZ",
    "8": "LONZ",
    "9": "RONZ"

}
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
    print(HUSKIES["27"])

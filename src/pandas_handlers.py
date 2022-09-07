import pandas as pd

from src.faceoff_data import HUSKIES


class FaceoffDataFrame:
    def __init__(self, husky):
        self.husky = husky
        self.df = pd.DataFrame
        self._make_columns(self.df)

    def _make_columns(self, df):
        self.df['husky'] = self.husky
        for opp in HUSKIES[self.husky]['vs']:
            self.df[opp] = opp


ex_huskies = {"27": {
    "vs": {
        "10": {
            "LD": {"w": 1, "l": 0},
            "RD": {"w": 0, "l": 0},
            "RO": {"w": 0, "l": 0},
            "LO": {"w": 0, "l": 0},
            "C": {"w": 0, "l": 0},
            "LDNZ": {"w": 0, "l": 0},
            "RDNZ": {"w": 2, "l": 0},
            "LONZ": {"w": 0, "l": 0},
            "RONZ": {"w": 0, "l": 1}
        },
        "12": {
            "LD": {"w": 0, "l": 0},
            "RD": {"w": 2, "l": 0},
            "RO": {"w": 0, "l": 0},
            "LO": {"w": 0, "l": 0},
            "C": {"w": 0, "l": 0},
            "LDNZ": {"w": 0, "l": 0},
            "RDNZ": {"w": 4, "l": 0},
            "LONZ": {"w": 0, "l": 2},
            "RONZ": {"w": 0, "l": 0}
        }
    }
}
}

# print(pd.read_json('huskies.json'))
print(pd.DataFrame.from_dict(data=ex_huskies['27']['vs']))

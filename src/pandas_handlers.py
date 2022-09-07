import pandas as pd

from src.faceoff_data import HUSKIES


class FaceoffDataFrame:
    def __init__(self, husky):
        self.husky = husky
        self.df = pd.DataFrame
        self._make_columns(self.df)

    def _make_columns(self, df):
        self.df['husky'] = self.husky
        for opp in HUSKIES[self.husky]:
            self.df[opp] = opp



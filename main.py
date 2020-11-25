import os
import pandas as pd
import numpy as np

from src.data import Data, DataTool
from src.regression import Regression

# Input data directory
DATA_DIR = './data'
OUT_DIR = './out'


def main():
    tesla_filename = os.path.join(DATA_DIR, 'TSLA.csv')
    hitachy_filename = os.path.join(DATA_DIR, './HTHIY.csv')  # Hitachi, Ltd.
    ivr_filename = os.path.join(DATA_DIR, './IYR.csv')  # iShares U.S. Real Estate ETF
    lithium_filename = os.path.join(DATA_DIR, './LIT.csv')  # Global X Lithium & Battery Tech ETF (LIT)

    # Read CSV files into Panda Dataframes
    r_y = Data(tesla_filename)
    y = r_y.to_panda('tesla')

    r_x1 = Data(hitachy_filename)
    x1 = r_x1.to_panda('hitachy')

    r_x2 = Data(lithium_filename)
    x2 = r_x2.to_panda('lithium')

    r_x3 = Data(ivr_filename)
    x3 = r_x3.to_panda('ivr')

    from functools import reduce
    data_frames = [x1.drop(['hitachy_price'], axis=1),
                   x2.drop(['lithium_price'], axis=1),
                   x3.drop(['ivr_price'], axis=1),
                   y.drop(['tesla_price'], axis=1)]

    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how='outer'), data_frames).fillna('void')

    # Get the correlation Matrix
    dt = DataTool(df_merged)
    dt.corr_matrix(OUT_DIR)

    #  Stack multiple independent variables, only keep the Returns columns
    x = np.vstack((x1['hitachy_returns'], x2['lithium_returns'], x3['ivr_returns']))
    x = x.T
    y = y['tesla_returns']

    # Apply linear regression
    regression = Regression()
    model = regression.createModel()
    model.fit(x, y)
    model.score(x, y)  # R-square

    import statsmodels.api as sm
    # By default statsmodel does not include intercept for regression (A in : y =  A + B*x1 + C*x2 )
    X = sm.add_constant(x)
    # Create Ordinary Least-Squares (OLS) model
    sm_model = sm.OLS(y, X)
    fit = sm_model.fit()

    # Save summary in pickle
    fit.save(OUT_DIR+"/fit_summary.pickle")

    with open(OUT_DIR+"/fit_summary.txt", 'w') as f:
        print(fit.summary(), file=f)

    print(fit.summary())


if __name__ == "__main__":
    main()

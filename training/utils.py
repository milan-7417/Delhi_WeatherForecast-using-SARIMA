import warnings
warnings.filterwarnings("ignore")

import numpy as np

from itertools import product

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)

from statsmodels.tsa.statespace.sarimax import SARIMAX


# =====================================================
# Search Best SARIMA Parameters
# =====================================================

def search_best_sarima(
    train_series,
    seasonal_period=30
):
    """
    Returns
    -------
    best_order
    best_seasonal_order
    """

    p = [0, 1]
    d = [0, 1]
    q = [0, 1]

    P = [0, 1]
    D = [0]
    Q = [0, 1]

    best_order = None
    best_seasonal = None

    best_aic = np.inf

    total_models = 0

    for order in product(p, d, q):

        for seasonal in product(P, D, Q):

            seasonal_order = (

                seasonal[0],

                seasonal[1],

                seasonal[2],

                seasonal_period,

            )

            try:

                model = SARIMAX(

                    train_series,

                    order=order,

                    seasonal_order=seasonal_order,

                    enforce_stationarity=False,

                    enforce_invertibility=False,

                )

                fitted = model.fit(

                    disp=False,maxiter=200

                )

                total_models += 1

                if fitted.aic < best_aic:

                    best_aic = fitted.aic

                    best_order = order

                    best_seasonal = seasonal_order

            except:

                continue

    print(f"Models Tried : {total_models}")

    print(f"Best AIC     : {best_aic:.2f}")

    print(f"Best Order   : {best_order}")

    print(f"Best Seasonal: {best_seasonal}")

    return (

        best_order,

        best_seasonal,

    )


# =====================================================
# Fit SARIMA
# =====================================================

def fit_sarima(

    series,

    order,

    seasonal_order,

):

    model = SARIMAX(

        series,

        order=order,

        seasonal_order=seasonal_order,

        enforce_stationarity=False,

        enforce_invertibility=False,

    )

    fitted = model.fit(

        disp=False

    )

    return fitted


# =====================================================
# Forecast
# =====================================================

def forecast(

    model,

    steps,

):

    return model.forecast(

        steps

    )


# =====================================================
# Evaluation
# =====================================================

def evaluate(

    actual,

    prediction,

):

    mae = mean_absolute_error(

        actual,

        prediction,

    )

    rmse = np.sqrt(

        mean_squared_error(

            actual,

            prediction,

        )

    )

    denominator = actual.replace(0, np.nan)

    mape = np.nanmean(

        np.abs(

            (actual - prediction) /

            denominator

        )

    ) * 100

    return {

        "MAE": round(mae, 3),

        "RMSE": round(rmse, 3),

        "MAPE": round(mape, 3),

    }
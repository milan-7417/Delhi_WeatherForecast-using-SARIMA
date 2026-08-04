import warnings
warnings.filterwarnings("ignore")

import json
import pandas as pd

from config import (
    CLEAN_DATA,
    MODELS_DIR,
    WEATHER_COLUMNS,
)

from utils import (
    search_best_sarima,
    fit_sarima,
    forecast,
    evaluate,
)

# ===========================================
# Create Directories
# ===========================================

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ===========================================
# Load Dataset
# ===========================================

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

df = pd.read_csv(CLEAN_DATA)

df["time"] = pd.to_datetime(df["time"])

# ===========================================
# Storage
# ===========================================

results = []

model_configs = {}

# ===========================================
# Train Models
# ===========================================

for column in WEATHER_COLUMNS:

    print("\n" + "=" * 60)
    print(f"Training : {column}")
    print("=" * 60)

    series = df[column]

    split = int(len(series) * 0.80)

    train = series.iloc[:split]

    test = series.iloc[split:]

    # ---------------------------------------
    # Search Best Parameters
    # ---------------------------------------

    order, seasonal = search_best_sarima(train)

    # ---------------------------------------
    # Fit Model
    # ---------------------------------------

    model = fit_sarima(

        train,

        order,

        seasonal

    )

    # ---------------------------------------
    # Forecast Test Set
    # ---------------------------------------

    prediction = forecast(

        model,

        len(test)

    )

    # ---------------------------------------
    # Evaluation
    # ---------------------------------------

    metrics = evaluate(

        test,

        prediction

    )

    print(f"Best Order      : {order}")
    print(f"Best Seasonal   : {seasonal}")

    print(f"MAE  : {metrics['MAE']}")
    print(f"RMSE : {metrics['RMSE']}")
    print(f"MAPE : {metrics['MAPE']}")

    # ---------------------------------------
    # Save Parameters
    # ---------------------------------------

    model_configs[column] = {

        "order": list(order),

        "seasonal_order": list(seasonal)

    }

    # ---------------------------------------
    # Store Metrics
    # ---------------------------------------

    results.append({

        "Parameter": column,

        "Order": str(order),

        "Seasonal": str(seasonal),

        "MAE": metrics["MAE"],

        "RMSE": metrics["RMSE"],

        "MAPE": metrics["MAPE"]

    })

# ===========================================
# Save Model Configuration
# ===========================================

config_path = MODELS_DIR / "model_config.json"

with open(

    config_path,

    "w"

) as f:

    json.dump(

        model_configs,

        f,

        indent=4

    )

print("\nModel Configuration Saved.")

# ===========================================
# Save Training Results
# ===========================================

results_df = pd.DataFrame(results)

results_path = MODELS_DIR / "training_results.csv"

results_df.to_csv(

    results_path,

    index=False

)

print("Training Results Saved.")

print("\n")
print("=" * 60)
print("Training Completed Successfully")
print("=" * 60)

print(results_df)
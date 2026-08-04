import pandas as pd

from config import RAW_DATA, CLEAN_DATA


def load_data():
    """
    Load Open-Meteo CSV.

    Skip the first 3 metadata rows.
    """

    print("Loading dataset...")

    df = pd.read_csv(
        RAW_DATA,
        skiprows=3
    )

    return df


def rename_columns(df):
    """
    Rename Open-Meteo columns to clean names.
    """

    df.columns = [
        "time",
        "temperature_max",
        "temperature_min",
        "precipitation",
        "wind_speed",
        "wind_direction",
        "cloud_cover",
        "dew_point",
        "humidity",
        "temperature_mean",
        "sunrise",
        "sunset",
        "pressure",
    ]

    return df


def convert_datetime(df):
    """
    Convert datetime columns.
    """

    df["time"] = pd.to_datetime(df["time"])

    df["sunrise"] = pd.to_datetime(df["sunrise"])

    df["sunset"] = pd.to_datetime(df["sunset"])

    return df


def sort_data(df):
    """
    Sort dataset by date.
    """

    df = df.sort_values("time").reset_index(drop=True)

    return df


def remove_duplicates(df):
    """
    Remove duplicate dates.
    """

    before = len(df)

    df = df.drop_duplicates(subset="time")

    after = len(df)

    print(f"Removed {before-after} duplicate rows.")

    return df


def handle_missing_values(df):
    """
    Fill missing values.
    """

    numeric_columns = [
        "temperature_max",
        "temperature_min",
        "temperature_mean",
        "humidity",
        "precipitation",
        "wind_speed",
        "wind_direction",
        "pressure",
        "cloud_cover",
        "dew_point",
    ]

    df[numeric_columns] = df[numeric_columns].interpolate()

    df[numeric_columns] = df[numeric_columns].ffill()

    df[numeric_columns] = df[numeric_columns].bfill()

    return df


def save_data(df):
    """
    Save cleaned dataset.
    """

    df.to_csv(CLEAN_DATA, index=False)

    print(f"\nSaved cleaned dataset to:\n{CLEAN_DATA}")


def preprocess():

    df = load_data()

    df = rename_columns(df)

    df = convert_datetime(df)

    df = sort_data(df)

    df = remove_duplicates(df)

    df = handle_missing_values(df)

    save_data(df)

    print("\nPreprocessing Completed Successfully!")


if __name__ == "__main__":

    preprocess()
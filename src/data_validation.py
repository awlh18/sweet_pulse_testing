import pandas as pd
import pandera as pa


def _validate_sales_df(sales_df):
    """
    Validate the structure and data types of sales_df.
    To be used with `scripts/prepare_sales.csv.py`.

    Parameters
    ----------
    sales_df: pd.DataFrame
        The DataFrame (sales_df) to validate.

    Returns
    -------
    None
        This function does not return anything. It will raise a SchemaError
        if the DataFrame does not conform to the expected schema.

    Raises
    ------
    pandera.errors.SchemaError
        If the DataFrame does not match the expected schema definition.
    """

    schema_features_df = pa.DataFrameSchema({
        "day_of_week": pa.Column(str,  pa.Check.isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])),
        "type_of_day": pa.Column(str, pa.Check.isin(["Weekday", "Weekend", "Friday", "Unusual", "Holiday"])),
        "month": pa.Column(str, pa.Check.isin(["January", "February", "March", "April", "May", "June", "July", "August", "September", 
                                                "October", "November", "December"])),
        "hours_opened": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
        "net_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "1x_items": pa.Column(float),
        "net_sales_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "tips_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "total_sales_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "in_store_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "pick_up_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "ubereats_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "taiyaki_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "soft_serve_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "drink_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "HFC_drink_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "drinks_sales_total": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "ICF?": pa.Column(bool),
        "HCF?": pa.Column(bool),
        "Kim\'s?": pa.Column(bool),
        "in_store_orders": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "pickup_orders": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
        "ubereats_orders": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
        "total_orders": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "sales_per_order": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    })

    schema_features_df.validate(sales_df)

def _validate_weather_df(weather_df):
    """
    Validate the structure and data types of weather_df.
    To be used with `scripts/prepare_weather.csv.py`.

    Parameters
    ----------
    weather_df: pd.DataFrame
        The DataFrame (weather_df) to validate.

    Returns
    -------
    None
        This function does not return anything. It will raise a SchemaError
        if the DataFrame does not conform to the expected schema.

    Raises
    ------
    pandera.errors.SchemaError
        If the DataFrame does not match the expected schema definition.
    """

    schema_features_df = pa.DataFrameSchema({
    "date": pa.Column(pa.DateTime, nullable=True),
    "avg_temperature": pa.Column(float, nullable=True),
    "rain": pa.Column(float, nullable=True),
    "snow": pa.Column(float, nullable=True)
    })

    schema_features_df.validate(weather_df)

def _validate_combined_df(combined_df):
    """
    Validate the structure and data types of combined_df.
    To be used with `scripts/prepare_combined.csv.py`.

    Parameters
    ----------
    combined_df: pd.DataFrame
        The DataFrame (combined_df) to validate.

    Returns
    -------
    None
        This function does not return anything. It will raise a SchemaError
        if the DataFrame does not conform to the expected schema.

    Raises
    ------
    pandera.errors.SchemaError
        If the DataFrame does not match the expected schema definition.
    """

    schema_features_df = pa.DataFrameSchema({
        "day_of_week": pa.Column(str, pa.Check.isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])),
        "type_of_day": pa.Column(str, pa.Check.isin(["Weekday", "Weekend", "Friday", "Unusual", "Holiday"])),
        "month": pa.Column(str, pa.Check.isin(["January", "February", "March", "April", "May", "June", "July", "August", "September", 
                                        "October", "November", "December"])),
        "hours_opened": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
        "net_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "1x_items": pa.Column(float),
        "net_sales_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "tips_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "total_sales_normalized": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "in_store_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "pick_up_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "ubereats_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "taiyaki_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "soft_serve_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "drink_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "HFC_drink_sales": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "drinks_sales_total": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "ICF?": pa.Column(bool),
        "HCF?": pa.Column(bool),
        "Kim\'s?": pa.Column(bool),
        "in_store_orders": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "pickup_orders": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
        "ubereats_orders": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
        "total_orders": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
        "avg_temperature": pa.Column(float, nullable=True),
        "rain": pa.Column(float, nullable=True),
        "snow": pa.Column(float, nullable=True),
        "is_long_weekend": pa.Column(bool),
        "is_holiday": pa.Column(bool),
        "season": pa.Column(pa.Category, pa.Check.isin(["Winter", "Spring", "Summer", "Fall"])),
        "date": pa.Column(pa.DateTime),
        "sales_per_order": pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    })

    schema_features_df.validate(combined_df)

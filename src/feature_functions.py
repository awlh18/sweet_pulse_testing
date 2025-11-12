# Core libraries
import numpy as np
import pandas as pd
import datetime
from typing import Union
import os
import sys

def get_season(dates: Union[datetime.date, pd.Series]) ->  Union[str, pd.Series]:
    """
    Assign season to a datetime value or a Series of datetime values.

    - Winter: December to February
    - Spring: March to May
    - Summer: June to August
    - Fall: September to November

    Parameters
    ----------
    dates : pd.Series or datetime.date
        - A pd.Series of datetime objects or a single datetime (datetime.date).

    Returns
    -------
    str or pd.Series
        - If input is a single datetime.date: returns the season name as a string.
        - If input is a pd.Series: returns a Series of season names (str), with the same index and named 'season'.
    
    Raises
    ------
    TypeError
        If the input is neither a datetime.date nor a pd.Series.

    Examples
    --------
    >>> get_season(pd.Series([datetime.date(2024, 1, 15), datetime.date(2024, 7, 10)]))
    0    Winter
    1    Summer
    Name: season, dtype: object

    >>> get_season(datetime.date(2024, 10, 10))
    'Fall'
    """

    def _season_of_date(date):
        month = date.month
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'

    if isinstance(dates, pd.Series):
        return dates.apply(_season_of_date).rename("season")
    elif isinstance(dates, datetime.date):
        return _season_of_date(dates)
    else:
        raise TypeError(f"Input must be datetime.date or pd.Series but got {type(dates)}")

def is_HCF(HCF_sales: Union[float, pd.Series]) -> Union[bool, pd.Series]:
    """
    Identify whether a day is part of Hot Chocolate Festival (HCF) based on sales value.

    A day is considered an HCF day if the HCF sales value is greater than 0.

    Parameters
    ----------
    HCF_sales : float or pd.Series
        - A single float value representing HCF sales on a day or a pd.Series of HCF sales values over multiple days.

    Returns
    -------
    bool or pd.Series
        - If input is a float: returns True if sales > 0, else False.
        - If input is a pd.Series: returns a boolean Series named 'is_HCF' indicating HCF days.

    Raises
    ------
    TypeError
        If the input is not a float or pd.Series.

    Examples
    --------
    >>> is_HCF(0.0)
    False

    >>> is_HCF(12.5)
    True

    >>> is_HCF(pd.Series([0.0, 5.0, 0.0]))
    0    False
    1     True
    2    False
    Name: is_HCF, dtype: bool
    """

    if isinstance(HCF_sales, pd.Series):
        HCF_days = HCF_sales > 0
        HCF_days.name = 'is_HCF'
        return HCF_days

    elif isinstance(HCF_sales, float):
        return HCF_sales > 0

    else:
        raise TypeError(f"Input must be a float or pd.Series but got {type(HCF_sales)}")
        

def is_holiday(date: Union[str, pd.Series]) -> Union[bool, pd.Series]:
    """
    Identify whether a given day or series of days is labeled as a holiday.

    Parameters
    ----------
    date : str or pd.Series
        - A single string representing a day type (e.g., 'Holiday', 'Weekday', 'Weekend'), or a pd.Series of such strings.

    Returns
    -------
    bool or pd.Series
        - If input is a string: returns True if the value is 'Holiday', else False.
        - If input is a pd.Series: returns a boolean Series where True indicates a holiday.

    Raises
    ------
    TypeError
        If the input is neither a string nor a pd.Series.

    Examples
    --------
    >>> is_holiday("Holiday")
    True

    >>> is_holiday("Weekend")
    False

    >>> is_holiday(pd.Series(["Holiday", "Weekday", "Holiday"]))
    0     True
    1    False
    2     True
    dtype: bool
    """
    if isinstance(date, pd.Series): 
        holidays = date.apply(lambda day: day == 'Holiday') 
        return holidays

    elif isinstance(date, str):
        return date == 'Holiday'

    else:
        raise TypeError(f"Input must be a str or pd.series but got {type(date)}")
    

def is_long_weekend(type_of_days: pd.Series) -> pd.Series:
    """
    Identify days that are part of a long weekend based on a pd.series of day types.

    A long weekend is defined as a sequence where a 'Holiday' is immediately preceded
    or followed by a 'Weekend'. 

    Parameters
    ----------
    type_of_days : pd.Series
        A pd.Series of strings representing the type of each day in chronological order.
        Expected values include 'Weekday', 'Weekend', and 'Holiday'.

    Returns
    -------
    pd.Series
        A boolean Series of the same length, where True indicates that the day is part of a long weekend.
        The Series is named 'is_long_weekend'.

    Examples
    --------
    >>> import pandas as pd
    >>> is_long_weekend(pd.Series(['Weekday', 'Holiday', 'Weekend', 'Weekend']))
    0    False
    1     True
    2     True
    3     True
    Name: is_long_weekend, dtype: bool
    """

    is_long_weekend_list = [False] * len(type_of_days)

    for i ,day in enumerate(type_of_days):

        if day == 'Holiday':
            prev_day = type_of_days[i-1] if i > 0 else None
            next_day = type_of_days[i+1] if i < len(type_of_days) - 1 else None 
            
            if prev_day == 'Weekend':
                is_long_weekend_list[i] = True
                is_long_weekend_list[i-1] = True
                is_long_weekend_list[i-2] = True
            
            if next_day == 'Weekend':
                is_long_weekend_list[i] = True
                is_long_weekend_list[i+1] = True
                is_long_weekend_list[i+2] = True
    
    return pd.Series(is_long_weekend_list, name='is_long_weekend')
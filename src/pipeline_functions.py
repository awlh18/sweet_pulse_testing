import pandas as pd

def process_sales(uploaded_sales_file):

    sales_df = pd.read_excel(uploaded_sales_file, index_col=0)

    # clean up values for boolean columns 
    sales_df['HCF?'] = sales_df['HCF?'].replace([0, 'Yes'], [False, True])
    sales_df['ICF?'] = sales_df['ICF?'].replace([0, 'Yes'], [False, True])
    sales_df['Kim\'s?'] = sales_df['Kim\'s?'].replace([0, 'Yes'], [False, True])
    sales_df['sales_per_order'] = sales_df['total_sales_normalized'] / sales_df['in_store_orders'] 
    sales_df['month'] = sales_df.index.month_name()

    # handle missing values 
    sales_df[sales_df.select_dtypes(include='number').columns] = sales_df.select_dtypes(include='number').fillna(0)
    sales_df[sales_df.select_dtypes(include='bool').columns] = sales_df.select_dtypes(include='bool').fillna(False)

    _validate_sales_df(sales_df)

    sales_df[sales_df.select_dtypes(include='number').columns] = sales_df.select_dtypes(include='number').round(1)
    print("Successfully prepared sales data!")

    return sales_df

def process_weather(uploaded_weather_file):

    weather_columns = ['date','avg_temperature', 'rain', 'snow']
    weather_df = pd.read_excel(uploaded_weather_file, index_col=0)

    weather_df = weather_df[weather_columns]

    # set date as datetime 
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    
    # handle missing values 
    weather_df[weather_df.select_dtypes(include='number').columns] = weather_df.select_dtypes(include='number').fillna(0)

    _validate_weather_df(weather_df)

    return weather_df

def process_combined(sales_df, weather_df):

    start_date=sales_df['date'].min()
    end_date=sales_df['date'].max()

    if not start_date in weather_df['date'].values:
        return print(f'Sales start date {start_date.date()} not in weather data. Please double weather data range.')
       
    if not end_date in weather_df['date'].values:
        return print(f'Sales end date {end_date.date()} not in weather data. Please double check weather data range.')

    condition = weather_df['date'].between(start_date, end_date)
    weather_df = weather_df[condition]

    combined_df = pd.merge(sales_df, weather_df, on='date', how='left')

    # create features 
    combined_df['is_long_weekend']=is_long_weekend(combined_df['type_of_day'])
    # combined_df['is_HCF']=is_HCF(combined_df['HCF_sales'])
    combined_df['is_holiday']=is_holiday(combined_df['type_of_day'])
    combined_df['season']=get_season(combined_df['date'])
    # combined_df['day_of_week']=combined_df['date'].dt.day_name()

    # set categories
    combined_df['day_of_week'] = pd.Categorical(combined_df['day_of_week'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    combined_df['season'] = pd.Categorical(combined_df['season'], categories=['Winter', 'Spring', 'Summer', 'Fall'])

    # data validation
    _validate_combined_df(combined_df)

    # drop unusual days
    unusual_days=combined_df[combined_df['type_of_day']=='Unusual'].index.to_list()
    combined_df=combined_df.drop(index=unusual_days)

    # train, test split
    train_df=combined_df.iloc[:-30]
    test_df=combined_df.iloc[-30:]
    
    return train_df, test_df 

def train_model_taiyaki(train_df):

    X_train = train_df.drop(columns=['taiyaki_sales'])
    y_train = train_df['taiyaki_sales']

    all_features = X_train.columns.to_list()
    numerical_features = ['avg_temperature', 'rain', 'snow']
    categorical_features = ['is_long_weekend', 'HCF?', 'ICF?', 'season', 'day_of_week', 'is_holiday', 'Kim\'s?']
    category_orders = [
    [False, True],  # is_long_weekend
    [False, True],  # is_HCF
    [False, True],  # is_ICF
    ['Winter', 'Spring', 'Summer', 'Fall'],  # season
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],  # day_of_week
    [False, True],  # is_holiday,
    [False, True]  # competitor
]
    drop_features = [f for f in all_features if f not in numerical_features + categorical_features]

    preprocessor = make_column_transformer(
    (OneHotEncoder(drop='first', categories=category_orders), categorical_features),
    (StandardScaler(), numerical_features),
    ("drop", drop_features)
    )

    lr_pipe = make_pipeline(preprocessor, LinearRegression())

    lr_pipe.fit(X_train, y_train)

    return lr_pipe 

def train_model_soft_serve(train_df): 


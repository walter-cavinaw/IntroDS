import numpy as np
import pandas
import statsmodels.api as sm
import datetime

"""
Here is the analysis for the New York Subway Data with relation to weather.
It includes the regression model used to predict hourly ridership and the comparison of ridership
on rainy and non-rainy days.
This also includes the prediction mechanism I used for Problem Set 3, Question 8.
"""


def predictions(weather_turnstile):
    """Predictions for Problem Set 3, Question 8"""
    # weather_turnstile['week_day'] = \
    # weather_turnstile['DATEn'].map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d').day)
    X = weather_turnstile[['rain', 'Hour', 'meantempi', 'maxtempi', 'meanpressurei']]
    y = weather_turnstile['ENTRIESn_hourly']
    dummy_units = pandas.get_dummies(weather_turnstile['UNIT'], prefix='unit')
    X = X.join(dummy_units)
    X = sm.add_constant(X)

    est = sm.OLS(y, X)
    est = est.fit()
    return est.predict(X)

# TODO: implement predictions for new turnstile_weather_v2 and get coefficient, including R^2


def predict(data):
    X = data[['rain']]

def main():
    print "start"
    df = pandas.read_csv("improved-dataset/turnstile_weather_v2.csv")
    print "done"

if __name__ == "__main__":
    main()
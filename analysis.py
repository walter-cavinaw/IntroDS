import pandas
import statsmodels.api as sm
import scipy
from ggplot import ggplot, geom_histogram, aes, xlab, ylab, ggtitle, geom_bar
import numpy

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


def predict(data):
    X = data[['rain', 'hour', 'day_week', 'weekday', 'wspdi', 'meanwspdi', 'fog', 'meantempi',  'tempi', 'precipi', 'meanprecipi', 'meanpressurei', 'pressurei']]
    dummy_units = pandas.get_dummies(data['UNIT'], prefix='unit')
    dummy_cond = pandas.get_dummies(data['conds'], prefix='conditions')
    X = X.join([dummy_units, dummy_cond])
    X = sm.add_constant(X)

    y = data['ENTRIESn_hourly']

    est = sm.OLS(y, X)
    est = est.fit()

    print est.summary()


def plot_histogram(data):
    plot = ggplot(data, aes(x='ENTRIESn_hourly', colour='factor(rain)', fill='factor(rain)')) + geom_histogram(binwidth=50) \
        + xlab('Entries per Hour') + ylab('Frequency') + ggtitle('Histogram of Subway Entries on Rainy vs Non-Rainy Days')
    print plot


def statistics(data):
    rain_df = data['ENTRIESn_hourly'][data['rain'] == 1]
    no_rain_df = data['ENTRIESn_hourly'][data['rain'] == 0]

    wr, pr = scipy.stats.shapiro(rain_df)
    wn, pn = scipy.stats.shapiro(no_rain_df)

    print "probability rain data is normal: " + str(pr) + ", " + str(wr)
    print "probability no-rain data is normal: " + str(pn) + ", " + str(wn)

    u, p = scipy.stats.mannwhitneyu(rain_df, no_rain_df)

    n1 = len(rain_df.index)
    n2 = len(no_rain_df.index)

    z = (u - (n1*n2/2))/(n1*n2*(n1+n2+1)/12)**0.5

    p = scipy.stats.norm.cdf(z)
    mean_rain = numpy.mean(rain_df)
    mean_no_rain = numpy.mean(no_rain_df)

    print "The probability that rain is equal to non-rain " + str(p)
    print "The mean of rain: " + str(mean_rain) + "\nThe mean of no-rain: " + str(mean_no_rain)


def plot_by_day(data):
    plot3 = ggplot(data, aes(x='day_week')) + geom_bar(aes(weight='ENTRIESn_hourly'))
    print plot3


def main():
    print "start"
    df = pandas.read_csv("improved-dataset/turnstile_weather_v2.csv")
    #predict(df)
    #plot_histogram(df)
    #statistics(df)
    plot_by_day(df)
    print "done"

if __name__ == "__main__":
    main()
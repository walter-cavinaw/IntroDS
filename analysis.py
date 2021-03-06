import pandas
import statsmodels.api as sm
import scipy
from ggplot import ggplot, geom_histogram, aes, xlab, ylab, ggtitle, geom_bar, scale_x_continuous
import numpy

"""
Here is the analysis for the New York Subway Data with relation to weather.
It includes the regression model used to predict hourly ridership and the comparison of ridership
on rainy and non-rainy days.
This also includes the prediction mechanism I used for Problem Set 3, Question 8.
"""


def predictions(weather_turnstile):
    """Predictions for Problem Set 3, Question 8"""
    X = weather_turnstile[['rain', 'hour', 'meantempi']]
    dummy_units = pandas.get_dummies(weather_turnstile['UNIT'], prefix='unit')
    X = X.join([dummy_units])
    X = sm.add_constant(X)

    y = weather_turnstile['ENTRIESn_hourly']

    est = sm.OLS(y, X)
    est = est.fit()
    print est.summary()


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
    rain_df = data[['ENTRIESn_hourly']][data['rain'] == 1]
    no_rain_df = data[['ENTRIESn_hourly']][data['rain'] == 0]

    wr, pr = scipy.stats.shapiro(rain_df['ENTRIESn_hourly'])
    wn, pn = scipy.stats.shapiro(no_rain_df['ENTRIESn_hourly'])
    #check ranksum
    print "probability rain data is normal: " + str(pr) + ", " + str(wr)
    print "probability no-rain data is normal: " + str(pn) + ", " + str(wn)

    u, p = scipy.stats.mannwhitneyu(rain_df['ENTRIESn_hourly'], no_rain_df['ENTRIESn_hourly'])

    n1 = len(rain_df.index)
    n2 = len(no_rain_df.index)

    z = (u - (n1*n2/2))/(n1*n2*(n1+n2+1)/12)**0.5

    p = scipy.stats.norm.cdf(z)
    mean_rain = numpy.mean(rain_df['ENTRIESn_hourly'])
    median_rain = numpy.median(rain_df['ENTRIESn_hourly'])
    mean_no_rain = numpy.mean(no_rain_df['ENTRIESn_hourly'])
    median_no_rain = numpy.median(no_rain_df['ENTRIESn_hourly'])
    print "rainy day data"
    print rain_df['ENTRIESn_hourly'].describe()
    print "\nnon-rainy data"
    print no_rain_df['ENTRIESn_hourly'].describe()

    print "The probability that rain is equal to non-rain " + str(p)
    print "The mean of rain: " + str(mean_rain) + "\nThe median of rain: " + str(median_rain) \
    + "\nThe mean of no-rain: " + str(mean_no_rain) + "\nThe median of no rain: " + str(median_no_rain)


def plot_by_day(data):
    dow_group = data.groupby('day_week').mean()['ENTRIESn_hourly']
    d = {'day_week': dow_group.index, 'ENTRIESn_hourly': dow_group.values}
    data = pandas.DataFrame(d)
    plot3 = ggplot(data, aes(x='day_week', y='ENTRIESn_hourly', width="0.8")) + \
            geom_bar(stat="bar") \
            + scale_x_continuous(name="Days of the Week",
                                 labels=["","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                                 limits=(-0.6, 6.6)) + ggtitle("Hourly Turnstile Entries By Day") \
            + ylab("Average Hourly Entries")
    print plot3


def plottest():
    df = pandas.DataFrame({"x":[1,2,3,4], "y":[1,3,4,2]})
    plot = ggplot(aes(x="x", y="y"), df) + geom_bar(aes(x="x"), stat="bar")
    print plot


def main():
    print "start"
    df = pandas.read_csv("improved-dataset/turnstile_weather_v2.csv")
    #predictions(df)
    #predict(df)
    #plot_histogram(df)
    statistics(df)
    #plot_by_day(df)
    #plottest()
    print "done"

if __name__ == "__main__":
    main()
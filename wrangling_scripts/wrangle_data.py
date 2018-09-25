import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.colors
from collections import OrderedDict
import requests


# default list of all countries of interest (top 10 economies)
country_default = OrderedDict([('Canada', 'CAN'), ('United States', 'USA'), 
  ('Brazil', 'BRA'), ('France', 'FRA'), ('India', 'IND'), ('Italy', 'ITA'), 
  ('Germany', 'DEU'), ('United Kingdom', 'GBR'), ('China', 'CHN'), ('Japan', 'JPN')])


def return_figures(countries=country_default):
    """Creates four plotly visualizations using the World Bank API

    Args:
        countries (dict): list of countries for filtering the data

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    # when the countries variable is empty, use the country_default dictionary
    if not bool(countries):
        countries = country_default

    # prepare filter data for World Bank API
    # the API uses ISO-3 country codes separated by ;
    country_filter = list(countries.values())
    country_filter = [x.lower() for x in country_filter]
    country_filter = ';'.join(country_filter)

    # World Bank indicators of interest for pulling data
    indicators = ['EN.ATM.GHGT.KT.CE', 'EN.ATM.CO2E.PC', 'SP.POP.TOTL', 'EG.FEC.RNEW.ZS']

    data_frames = [] # stores the data frames with the indicator data of interest
    urls = [] # url endpoints for the World Bank API

    # pull data from World Bank API and clean the resulting json
    # results stored in data_frames variable
    for indicator in indicators:
        url = 'http://api.worldbank.org/v2/countries/' + country_filter + '/indicators/' + indicator +\
              '?date=1970:2012&per_page=1000&format=json'
        urls.append(url)

        try:
           r = requests.get(url)
           data = r.json()[1]
        except:
           print('could not load data ', indicator)
               
        # select value from dictionary for 'indicator' and 'country' columns
        for i, value in enumerate(data):
            value['indicator'] = value['indicator']['value']
            value['country'] = value['country']['value']
        
        data_frames.append(data)
        
    # first chart plots total greenhouse gas emission from 1970 to 2012 in top 10 economies 
    # as a line chart
    
    graph_one = []
    df_one = pd.DataFrame(data_frames[0])
    
    # put the countries in decreasing order by their values in 2014
    df_one_2012 = df_one[df_one['date'] == '2012'].sort_values('value', ascending=False)

    # this  country list will be re-used by all the charts to ensure legends have the same
    # order and color
    countrylist = df_one_2012.country.unique().tolist()
    
    # now sort df_one by date in ascending order
    df_one.sort_values('date', ascending=True, inplace=True)
    
    for country in countrylist:
        x_values = df_one[df_one['country'] == country].date.tolist()
        y_values = df_one[df_one['country'] == country].value.tolist()
        graph_one.append(
            go.Scatter(
                x = x_values,
                y = y_values,
                mode = 'lines',
                name = country
            )
        )
        
    layout_one = dict(title = 'Total greenhouse gas emissions per year',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'kt of CO2 equivalent'),
                )

    # second chart plots CO2 emissions per capita for 1970 and 2012
    graph_two = []
    df_two = pd.DataFrame(data_frames[1])
    df_two = df_two[(df_two.date == '1970') | (df_two.date == '2012')]
    df_two.sort_values('date', ascending=True, inplace=True)
    
    for country in countrylist:
        x_values = df_two[df_two['country'] == country].date.tolist()
        y_values = df_two[df_two['country'] == country].value.tolist()

        graph_two.append(
            go.Scatter(
                x = x_values,
                y = y_values,
                mode = 'lines',
                name = country
            )
        )

    layout_two = dict(title = 'CO2 emissions per capita',
                      xaxis = dict(title = 'Year',),
                      yaxis = dict(title = 'Metric tons per capita'),
                     )


    # third chart total population from 1970 to 2012
    graph_three = []
    df_three = pd.DataFrame(data_frames[2])
    df_three.sort_values('date', ascending=True, inplace=True)
    
    for country in countrylist:
        x_values = df_three[df_three['country'] == country].date.tolist()
        y_values = df_three[df_three['country'] == country].value.tolist()
    
        graph_three.append(
        go.Scatter(
            x = x_values,
            y = y_values,
            mode = 'lines',
            name = country
            )
        )

    layout_three = dict(title = 'Total population per year',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Population')
                       )
    
# fourth chart plots renewable energy consumption for 2012
    graph_four = []
    df_four = pd.DataFrame(data_frames[3])
    df_four_2012 = df_four[df_four['date'] == '2012']
    
    y_values = []
    for country in countrylist:
        y = df_four_2012[df_four_2012['country'] == country].value.tolist()[0]
        y_values.append(y)
    
    graph_four.append(
      go.Bar(
      x = countrylist,
      y = y_values,
      )
    )

    layout_four = dict(title = 'Renewable energy consumption in 2012',
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = '% of total energy consumption'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures
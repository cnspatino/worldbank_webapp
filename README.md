# Link to data dashboard web app: https://patino-worldbank-app.herokuapp.com/

# worldbank_webapp
World Bank Data Dashboard using the World Bank API

### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>
This code runs using Python versions 3.*. Additional python packages needed for this code are included in the requirements.txt file.

The packages can be installed by typing the following into your terminal (on a MacOS/Linux system):

`pip install -r requirements.txt`

## Project Motivation <a name="motivation"></a>
My motivation for this project was to practice web development and deployment using bootstrap, plotly, and flask. As for the data I chose to display, I was interested in exploring the following questions:

1. What are the trends in greenhouse gas emissions over time for countries with the top 10 economies?
2. What are the trends in CO2 emissions per capita for these countries over time?
3. How has the total population of these countries changed over time?
4. Which of these countries had the greatest and least percentage of renewable energy consumption?

## File Descriptions <a name="files"></a>
This repository includes all of the files that were necessary to code and deploy the web app.

The index.html file can be found in the worldbankapp/templates folder. This file includes the HTML and Bootstrap code for designing the web page.

The wrangle.py file in the wrangling_scripts folder contains the code for obtaining the data using the World Bank API and the pandas code for getting it in the right format to use with Plotly. It then includes the code for setting up the visualizations in Plotly.

The requirements.txt file includes all the necessary libraries for this project.

## Licensing, Authors, and Acknowledgements <a name="licensing"></a>
I'd like to thank the Udacity Data Science Nanodegree team for the inspiration and template code for this project. The template code can be found in [this github repository](https://github.com/udacity/DSND_Term2/tree/master/lessons/WebDevelopment/AdvancedDataDashboardCode/world_bank_api_dashboard).

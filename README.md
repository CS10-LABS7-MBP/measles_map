# Exploring infections through data: Interactive visualisation of Measles in the USA

Welcome to my project exploring interactive data visualisation in Python using Measles data from Project Tycho. The original dataset can be found on Kaggle here https://www.kaggle.com/pitt/contagious-diseases/home

Please find a conda enviroment file for all dependancies for this project. The project contains four parts:
* Exploring measles with interactive plots - this is the main project notebook
* Pandas Tutorial - a simple tutorial on Pandas that explains how I performed some of the data wrangling
* Bokeh Tutorial - an overview of some of the basic concepts of Bokeh that I used
* Dashboard application - the full bokeh python app that can be hosted locally using Bokeh Server

Dashboard application is also hosted remotely here - https://measles-bokeh.herokuapp.com/main

## Information for new programmers

If you do not have Python installed locally, I recommend starting with the Anaconda distribution. This will come preloaded with a whole bunch of libraries commonly used in the Data Science world. It also comes with the Jupyter Notebook software, as well as a whole bunch of other tools.

Download Anaconda using the link below and follow the installation instructions: https://www.anaconda.com/download

I would also recommend downloading Git, ther version control software behind GitHub.

The code in this project has three main dependancies:

* Pandas (comes preloaded with Anaconda)
* Seaborn
* BokehJS

To install a package to the core enviroment of your PC, use the following command

`conda install PACKAGE_NAME`

For example, to install Seaborn and BokehJS, execute the following commands in the command line:

`conda install seaborn`

`conda install bokeh`

To download the code for this project, we want to navigate to my GitHub page, and download from the link here:

https://github.com/burtonbiomedical/measles_map

If you have Git installed locally and are comfortable in doing so, please clone the repository using the following command:

`git clone https://github.com/burtonbiomedical/measles_map.git`

Otherwise, complete the following:

Click "Clone or Download"
Click "Download Zip"

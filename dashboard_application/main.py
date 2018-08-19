#Import pandas for data wrangling
import pandas as pd

#Import bokeh
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

#Import scripts for tabs
from scripts.line import line_tab
from scripts.map_bar import map_bar_tab

#Import data
from bokeh.sampledata.us_states import data as States
measles = pd.read_csv("measles.csv")
#Create columns for Year and Week_Number
measles["year"] = measles["week"].apply(lambda x: int(str(x)[0:4]))
measles["week_num"] = measles["week"].apply(lambda x: int(str(x)[4:7]))
measles.drop("week", axis = 1, inplace = True)
#Create states lookup dict
states = {
        state["name"].upper(): state for code, state in States.items() if state["name"] not in ["Hawaii", "Alaska"]
    }

#Define function for summarising data
def summarise(df, group_by):
    #Group data
    grouped = df.groupby(by = group_by)
    #Summarise data as Series then convert back to Dataframe
    cases_sum = pd.DataFrame(grouped["cases"].sum()).reset_index()
    cases_avg = pd.DataFrame(grouped["cases"].mean()).reset_index()
    avg_incidence_year = pd.DataFrame(grouped["incidence_per_capita"].mean()).reset_index()
    #Give columns sensible names
    avg_incidence_year = avg_incidence_year.rename(columns = {"incidence_per_capita": "avg_incidence_per_week"})
    cases_sum = cases_sum.rename(columns = {"cases": "total_cases_per_year"})
    cases_avg = cases_avg.rename(columns = {"cases": "avg_cases_per_week"})
    #Merge dataframes
    cases = pd.merge(cases_avg, cases_sum)
    new_df = pd.merge(avg_incidence_year, cases)
    return new_df

#Create yearly data
measles_yearly_data = summarise(measles, group_by = ["year", "state_name"])

#Add state boundary data
def state_data(df):
    df_ = df[~df["state_name"].isin(["HAWAII", "ALASKA"])]
    for z in ["lons", "lats"]:
        df_[z] = df_["state_name"].apply(lambda x: states[x][z])
    return df_

measles_yearly_data = state_data(measles_yearly_data)

#Dataframe for total cases per week
total_weekly = summarise(measles, ["week_num", "year"])

#Get tabs
tab1 = map_bar_tab(measles_yearly_data)
tab2 = line_tab(measles ,total_weekly)

#Put all the tabs together
tabs = Tabs(tabs = [tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)

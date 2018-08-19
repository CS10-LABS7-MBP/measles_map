from bokeh.plotting import figure
from bokeh.models import LogColorMapper, ColumnDataSource, HoverTool, LinearColorMapper, ColorBar, Panel
from bokeh.models.widgets import Select, Slider, Tabs, Select
from bokeh.layouts import column, row, WidgetBox
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.transform import factor_cmap

def map_bar_tab(source):
    
    def create_data(source, year):
        df = source[source["year"] == year]
        df = df.dropna()
        assert len(df) > 0, "No data for this disease and year combination"
        
        data = dict(
            state_name = df["state_name"],
            x = df['lons'].values.tolist(),
            y = df['lats'].values.tolist(),
            incidence_per_capita = df["avg_incidence_per_week"],
            total_cases = df["total_cases_per_year"],
            avg_cases = df["avg_cases_per_week"],
            year = df["year"]
        )
        
        return ColumnDataSource(data)
        
    def cases_bar_plot(src):
        states = src.data["state_name"]
        bar = figure(plot_width=550, plot_height=350, 
                     title="Total cases of Measles in the United States",
               x_range=states, toolbar_location=None, tools="", y_range = (0, 110000))
        bar.xgrid.grid_line_color = None
        bar.xaxis.axis_label = "US States"
        bar.xaxis.major_label_orientation = 1.2
        bar.yaxis.axis_label = "Total measle cases"

        bar.vbar(x='state_name', top='total_cases', width=1, source=src,
               line_color="white", fill_color="#3d84f7", 
               hover_line_color="black")
        bar.add_tools(HoverTool(tooltips=[("Average incidence per capita per week", "@incidence_per_capita")]))

        return bar
    
    def incidence_bar_plot(src):
        states = src.data["state_name"]
        bar = figure(plot_width=550, plot_height=350, 
                     title="Average weekly incidence of Measles in the United States",
               x_range=states, toolbar_location=None, tools="", y_range = (0, 62))
        bar.xgrid.grid_line_color = None
        bar.xaxis.axis_label = "US States"
        bar.xaxis.major_label_orientation = 1.2
        bar.yaxis.axis_label = "Average weekly incidence per capita"

        bar.vbar(x='state_name', top='incidence_per_capita', width=1, source=src,
               line_color="white", fill_color="#3d84f7", 
               hover_line_color="black")
        bar.add_tools(HoverTool(tooltips=[("Total Measles cases", "@total_cases")]))

        return bar
    
    def build_map(src):

        TOOLS = "pan,wheel_zoom,reset,hover,save"
        colors = ["#A7D49B", "#92AC86", "#696047", "#55251D", "#5A1807"]
        color_mapper = LinearColorMapper(palette=colors, low=src.data["incidence_per_capita"].min(), high=src.data["incidence_per_capita"].max())
        p = figure(
            title="US States", tools=TOOLS,
            x_axis_location=None, y_axis_location=None,
            tooltips=[
                ("Name", "@state_name"), ("Average incidences per capita per week", "@incidence_per_capita{1.11}"), 
                ("Average # of cases per week", "@avg_cases{1.11}"), ("Total cases in year", "@total_cases{1.11}")
            ], plot_width=850, plot_height=650)
        p.grid.grid_line_color = None
        p.hover.point_policy = "follow_mouse"
        p.patches('x', 'y', source=src, hover_line_color="black",
                  fill_color={'field': 'incidence_per_capita', 'transform': color_mapper},
                  fill_alpha=0.7, line_color="white", line_width=0.5)

        return p
    
    def update_map(attr, old, new):
        chosen_year = choose_year.value
        new_data = create_data(source, chosen_year)
        src.data.update(new_data.data)
        
    #Define Widgets
    choose_year = Slider(start=1928, end=2002, value=1928, step = 1, title = "Year")
    choose_year.on_change('value', update_map)
    
    #Select starting data
    src = create_data(source, 1928)
    
    #Init plot and set layout
    controls = WidgetBox(choose_year)
    m = build_map(src)
    b_cases = cases_bar_plot(src)
    b_incidence = incidence_bar_plot(src)
    layout = row(column(controls, m), column(b_cases, b_incidence))
    tab = Panel(child = layout, title = "Measles Map")
    return tab    
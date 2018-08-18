def dashboard_line(app):
    
    def create_data(year, state):
        df = measles[(measles["year"] == year) & (measles["state_name"] == state)]
        totals = total_weekly[total_weekly["year"] == year]
        #Remove missing weeks
        weeks_in_both = set(df["week_num"]).intersection(totals["week_num"])
        df = df[df["week_num"].isin(weeks_in_both)]
        totals = totals[totals["week_num"].isin(weeks_in_both)]
        assert len(df) > 0, "No data for this state and year combination"
        data = dict(
            state_name = df["state_name"],
            incidence_per_capita_state = df["incidence_per_capita"],
            total_cases_state = df["cases"],
            incidence_per_capita_total = totals["avg_incidence_per_week"],
            total_cases_total = totals["total_cases_per_year"],
            avg_cases_total = totals["avg_cases_per_week"],
            year = df["year"],
            week_num = df["week_num"]
        )
        
        return ColumnDataSource(data)

    def line_plot(src, chosen_state):
        line = figure(x_range = (1,52), plot_width=800, plot_height=500,
                      title="Incidence of Measles", 
                      toolbar_location=None, tools="")
        line.line(x="week_num", y="incidence_per_capita_total", line_width=2, source = src, line_color="red", legend = "National weekly average incidence per capita")
        line.line(x="week_num", y="incidence_per_capita_state", line_width=2, source = src, legend = "State weekly incidence per capita")
        line.xaxis.axis_label = "Week number"
        line.yaxis.axis_label = "Incidence per capita"
        line.circle(x="week_num", y="incidence_per_capita_state", size=12, 
                    fill_color="grey", hover_fill_color="firebrick",
                    fill_alpha=0.5, hover_alpha=0.8,
                    line_color=None, hover_line_color="white", source = src)
        line.circle(x="week_num", y="incidence_per_capita_total", size=12, 
            fill_color="firebrick", hover_fill_color="firebrick",
            fill_alpha=0.3, hover_alpha=0.5,
            line_color=None, hover_line_color="white", source = src)

        line.add_tools(HoverTool(tooltips=[("Total cases (state)","@total_cases_state"), ("Total cases (national)", "@total_cases_total"),("Week", "@week_num")]))
        return line
    
    def update_map(attr, old, new):
        chosen_year = choose_year.value
        chosen_state = choose_state.value
        new_data = create_data(chosen_year, chosen_state)
        src.data.update(new_data.data)
        
    #Define Widgets
    choose_year = Slider(start=1928, end=2002, value=1928, step = 1, title = "Year")
    choose_year.on_change('value', update_map)
    states = measles["state_name"].unique()
    menu = [(state, state) for state in states]
    choose_state = Select(options=menu, value="NEW YORK", title="Choose a US State")
    choose_state.on_change('value', update_map)
    
    
    #Select starting data
    src = create_data(1928, "NEW YORK")
    
    #Init plot and set layout
    controls = WidgetBox(choose_year, choose_state)
    l = line_plot(src, choose_state.value)
    layout = column(controls, l)
    app.add_root(layout)
    
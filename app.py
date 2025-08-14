import pandas as pd
import streamlit as st

def load_data():
    df = pd.read_excel("air_crashes_cleaned_data.xlsx")
    return df
try:
    df = load_data()
    #st.warning("💡 For best viewing experience, it's advisable to use **Dark Mode** for better visualization.")


    st.title("Air Crashes App")

    filters = {
    "Year": df["Year"].unique(),
    "Month": df["Month"].unique(),
    "Aircraft": df["Aircraft"].unique(),
    "Aircraft Manufacturer": df["Aircraft Manufacturer"].unique(),
    "Country": df["Country"].unique(),
}

    selected_filters = {}

    # Creating filters in sidebar dynamically
    for key, options in filters.items():
    
      selected_filters[key] = st.sidebar.multiselect(key, sorted(options))

    # Filtered data
    filtered_df = df.copy()
    for key, selected_values in selected_filters.items():
     if selected_values:
        filtered_df = filtered_df[filtered_df[key].isin(selected_values)]

    # KPIs
    total_crashes = len(filtered_df)
    total_fatalities = filtered_df["total_fatalities"].sum()
    total_passengers = filtered_df["Aboard"].sum()
    total_survivors = filtered_df["Survivors"].sum()
    

    #streamlit column components
    col1 , col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Crashes", total_crashes)

    with col2:
        st.metric("Total Fatalities", f"{total_fatalities:,}")

    with col3:
        st.metric("Total Passengers", f"{total_passengers:,}")
    
    with col4:
        st.metric("Total Survivors", f"{total_survivors:,}")
    

    # display the Filtered Table 
    st.dataframe(filtered_df)

    st.write("### Analysis Findings")
    # RQ1
    st.write("#### 1. Number of Air crashes per year")
    # Full list for table
    temp1 = (
    filtered_df.groupby("Year").size().reset_index(name="Crash Count")
    .sort_values("Crash Count", ascending=False)
    )
    st.dataframe(temp1)
    # Top 10 for chart
    temp1c= temp1.head(10)


     # plotting a bar chart
    import altair as alt
    chart1 = alt.Chart(temp1c).mark_bar().encode(
        x=alt.X("Year:N",
            sort=alt.SortField(field="Crash Count", order="descending"),
            axis=alt.Axis(title="Year", labelAngle=45),
        ),
        y=alt.Y("Crash Count:Q", axis=alt.Axis(title="Number of Air Crashes")),
        color=alt.Color("Crash Count:Q", legend=None),
        tooltip=["Year:N", "Crash Count:Q"],
    ).properties( height=320)
    
    # displaying the chart
    st.altair_chart(chart1, use_container_width=True)

    #RQ2
    st.write("#### 2. Total fatalities(both ground & air) per year.")
    temp2 = (
    filtered_df.groupby("Year", as_index=False)["total_fatalities"]
      .sum()
      .sort_values(by="total_fatalities", ascending=False)
    )
    st.dataframe(temp2)
    # for chart
    temp2c = temp2.head(10)

    # plotting chart
    chart2 = alt.Chart(temp2c).mark_bar().encode(
        y=alt.Y("Year:N",sort=alt.SortField(field="total_fatalities", order="descending"),axis=alt.Axis(title="Year", labelAngle=45)),
        x=alt.X("total_fatalities:Q",axis=alt.Axis(title="Total Fatalities")),
        color=alt.Color("total_fatalities:Q", legend=None),
        tooltip=["Year:N", "total_fatalities:Q"]
    ).properties(height=320)
    
    # displaying the chart
    st.altair_chart(chart2, use_container_width=True)

    #RQ3
    import matplotlib.pyplot as plt
    import seaborn as sns

    st.write("#### 3. Relationship Between the Total Number of People Aboard and the Number of Survivors")

    # Prepare data
    temp3 = filtered_df.dropna(subset=["Aboard", "Survivors"]).copy()
    temp3["Aboard"] = pd.to_numeric(temp3["Aboard"], errors="coerce")
    temp3["Survivors"] = pd.to_numeric(temp3["Survivors"], errors="coerce")
    temp3 = temp3.dropna(subset=["Aboard", "Survivors"])
    st.dataframe(temp3[["Year", "Aboard", "Survivors"]])

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    

    # Scatter plot
    sns.scatterplot(
       data=temp3,
       x="Aboard",
       y="Survivors",
       hue="Year",
       palette="viridis",
       alpha=0.7,
       edgecolor="w",
       s=80,
       ax=ax
    )

    # Regression line
    sns.regplot(
       data=temp3,
       x="Aboard",
       y="Survivors",
       scatter=False,   
       color="red",
       line_kws={"linewidth": 2},
       ax=ax
)

    ax.set_xlabel("Number of Passengers Aboard", fontsize=12)
    ax.set_ylabel("Number of Survivors", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(title="Year", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Show chart in Streamlit
    st.pyplot(fig)


    #RQ4

    import altair as alt

    st.write("#### 4.  Monthly Air Crash Patterns")

    # Month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    # Grouping
    monthly_crashes = (

       filtered_df.groupby('Month')
       .size()
       .reindex(month_order)
       .reset_index(name='Crash Count')
    )
    st.dataframe(monthly_crashes)

    # Bar chart
    bars = alt.Chart(monthly_crashes).mark_bar().encode(
       x=alt.X('Month:N', sort=month_order, axis=alt.Axis(title='Month', labelAngle=45)),
       y=alt.Y('Crash Count:Q', axis=alt.Axis(title='Number of Crashes')),
       color=alt.Color('Crash Count:Q', scale=alt.Scale(scheme='viridis'), legend=None),
       tooltip=['Month:N', 'Crash Count:Q']
    )

    # Line + points
    line = alt.Chart(monthly_crashes).mark_line(color='red', point=alt.OverlayMarkDef(color='red', size=60)).encode(
       x=alt.X('Month:N', sort=month_order),
       y='Crash Count:Q'
    )

    # Combine charts
    chart4 = (bars + line).properties(
       height=350
    ).configure_axis(
       grid=True,
       gridOpacity=0.2
    ).configure_view(
       strokeWidth=0  # removes border outline
    )

    st.altair_chart(chart4, use_container_width=True)

    # RQ5
    st.write("#### 5. Crash Distribution by Quarter")

    # Match exactly what is in the dataset
    quarter_order = ['Qtr 1', 'Qtr 2', 'Qtr 3', 'Qtr 4']

    # Grouping by quarter and counting crashes
    quarterly_crashes = (
       filtered_df.groupby('Quarter')
       .size()
       .reindex(quarter_order, fill_value=0)  # fill_value=0 ensures missing quarters get 0
       .reset_index(name='Crash Count')
    )

    # Show DataFrame
    st.dataframe(quarterly_crashes)

    # Getting Seaborn's coolwarm palette and convert to hex
    palette = sns.color_palette("coolwarm", n_colors=len(quarter_order)).as_hex()

    # Creating Altair bar chart
    chart5 = (alt.Chart(quarterly_crashes).mark_bar().encode(
       x=alt.X("Quarter", sort=quarter_order, axis=alt.Axis()),
       y=alt.Y("Crash Count", axis=alt.Axis()),
       color=alt.Color("Quarter", scale=alt.Scale(domain=quarter_order, range=palette), legend=None)
    ).properties(width=500, height=300)
    )

    # Display the chart
    st.altair_chart(chart5, use_container_width=True)



    # RQ6
    import squarify
    st.write("#### 6.  Top 5 Countries by Number of Deaths")
    # # Data
    top5_countries = (filtered_df.groupby('Country')['total_fatalities'].sum().sort_values(ascending=False).head(5).reset_index()
    )
    st.dataframe(top5_countries)
    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    sizes = top5_countries['total_fatalities']
    labels = [f"{country}\n{deaths:,}" 
              for country, deaths in zip(top5_countries['Country'], sizes)]
    # Transparent background
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    squarify.plot(
       sizes=sizes,
       label=labels,
       color=sns.color_palette('Reds', len(sizes)),
       alpha=0.8,
       text_kwargs={'color': 'white', 'fontsize': 12, 'weight': 'bold'}
    )

    # Remove axes
    ax.axis('off')
    

    # Show in Streamlit
    st.pyplot(fig)

    # RQ7
    st.write("#### 7.  Top 10 Most Crash-Prone Aircraft Manufacturers")

    # Grouping by Aircraft Manufacturer and count crashes
    manufacturer_counts = (filtered_df['Aircraft Manufacturer'].value_counts().head(10).reset_index())
    manufacturer_counts.columns = ['Aircraft Manufacturer', 'Crash Count']

    # Show DataFrame
    st.dataframe(manufacturer_counts)

    # Bar chart
    chart7 = (alt.Chart(manufacturer_counts).mark_bar().encode(
       x=alt.X("Crash Count:Q", title="Number of Crashes"),
       y=alt.Y("Aircraft Manufacturer:N", sort='-x', title="Aircraft Manufacturer"),
       color=alt.Color("Crash Count:Q", scale=alt.Scale(scheme="reds"), legend=None),
       tooltip=["Aircraft Manufacturer:N", "Crash Count:Q"]
    ).properties(height=400)
    .configure_axis(
       grid=True,
       gridOpacity=0.2
       ).configure_view(strokeWidth=0)  # removes border
)

    # displaying chart
    st.altair_chart(chart7, use_container_width=True)

    #RQ8
    st.write("#### 8. Frequent Aircraft Types in Crashes")

    # Grouping by 'Aircraft' and count
    aircraft_counts = (filtered_df['Aircraft'].value_counts().head(10).reset_index())
    aircraft_counts.columns = ['Aircraft', 'Crash Count']

    # Show DataFrame
    st.dataframe(aircraft_counts)

    # plotting chart
    chart8 = (alt.Chart(aircraft_counts).mark_bar().encode(
       x=alt.X("Crash Count:Q", title="Number of Crashes"),
       y=alt.Y("Aircraft:N", sort='-x', title="Aircraft Type"),
       color=alt.Color("Crash Count:Q", scale=alt.Scale(scheme="blues"), legend=None),
       tooltip=["Aircraft:N", "Crash Count:Q"]
       ).properties(height=400)
       .configure_axis(
          grid=True,
          gridOpacity=0.2
            )
            .configure_view(strokeWidth=0)  # removes border
            )

         # display in Streamlit
    st.altair_chart(chart8, use_container_width=True)

    # RQ9
    st.write("#### 9. Aircraft with the highest number of survivors")

    # Grouping by Aircraft and summing survivors
    survivor_counts = (filtered_df.groupby("Aircraft")["Survivors"].sum().sort_values(ascending=False).head(5)
                       .reset_index()
                       )

    # Calculate percentage for labels
    survivor_counts["Percentage"] = (
       survivor_counts["Survivors"] / survivor_counts["Survivors"].sum() * 100).round(0).astype(int).astype(str) + '%'
    # displaying the dataframe
    st.dataframe(survivor_counts)

    # Creating a donut chart with Altair
    donut_chart = (alt.Chart(survivor_counts).mark_arc(innerRadius=60)  # innerRadius makes it a donut
                   .encode(
                      theta=alt.Theta("Survivors:Q", stack=True),
                      color=alt.Color("Aircraft:N", scale=alt.Scale(scheme="set2"), legend=alt.Legend(title="Aircraft",direction="vertical",orient="right"),),
                      tooltip=[
                         "Aircraft:N",
                           alt.Tooltip("Survivors:Q", format=","),
                           alt.Tooltip("Percentage:Q", format=".0f")
                           ]).properties(height=400)
                           )

    # Adding labels in the center of each arc
    percentage_labels = (alt.Chart(survivor_counts).mark_text(radius=90, size=14).encode(
       text=alt.Text("Percentage:N"),
       theta=alt.Theta("Survivors:Q", stack=True)
       )
       )

    # Combining the  chart and labels
    st.altair_chart(donut_chart + percentage_labels, use_container_width=True)

    # RQ10
    st.write("#### 10. Top 10 Aircraft Types by Total Passengers Aboard")
    # Grouping by Aircraft and summing passengers aboard
    passenger_counts = (df.groupby("Aircraft")["Aboard"].sum().sort_values(ascending=False).head(10).reset_index())

    # Display DataFrame before chart
    st.dataframe(passenger_counts)

    # Altair horizontal bar chart
    bar_chart = (
       alt.Chart(passenger_counts).mark_bar().encode(
          x=alt.X("Aboard:Q", title="Total Passengers Aboard"),
          y=alt.Y("Aircraft:N", sort='-x', title="Aircraft"),
          color=alt.Color(
             "Aboard:Q",scale=alt.Scale(scheme="blues"),  # Gradient like Seaborn "Blues_r"
             legend=None
        ),
        tooltip=[
           alt.Tooltip("Aircraft:N"),
           alt.Tooltip("Aboard:Q", format=",")
        ]
    ).properties(height=400)
    )

    # Adding labels to bars
    labels = (alt.Chart(passenger_counts).mark_text(align="left", baseline="middle", dx=3).encode(
       x="Aboard:Q",
       y=alt.Y("Aircraft:N", sort='-x'),
       text=alt.Text("Aboard:Q", format=",")
       )
       )

    # Combining chart+labels and displaying in Streamlit
    st.altair_chart(bar_chart + labels, use_container_width=True)











    




    

except Exception as e:
    st.error("Error: check error details")

    with st.expander("Error Details"):
        st.code(str(e))
        # st.code (traceback.format.exc())

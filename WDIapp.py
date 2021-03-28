import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache
def getCountryTable(countries):
    ct = data[data["Country Name"].isin(countries)]
    ct = ct.drop(columns=["Unnamed: 65"])
    
    year_list = []
    for i in range(1960,2021):
        year_list.append(str(i))
        
    data_present = ((len(year_list) - ct[year_list].isnull().sum(axis=1))/len(year_list))*100
    ct["Data Present in %"] = data_present

    cols = ct.columns.to_list()
    cols2 = cols[:4] + cols[-1:] + cols[5:-1]
    
    return ct[cols2]

@st.cache
def getIndicatorList(countries,data_present):
    df = getCountryTable(countries)
    return df[df["Data Present in %"] >= int(data_present)]["Indicator Name"].to_list()

@st.cache
def getCountryComparisonPlot(country_list,indicator_list,enableLegend):
        ct = data[data["Country Name"].isin(country_list)]
        ct = ct.drop(columns=["Unnamed: 65"])
        ct.reset_index(inplace=True)
        ct.set_index(["Country Name","index"],inplace=True)

        year_list = []
        for i in range(1960,2021):
            year_list.append(str(i))
    

        ct2 = ct.loc[ct["Indicator Name"].isin(indicator_list)][year_list].T
    
        fig2 = go.Figure()

        for col in ct2.columns:
            fig2.add_scatter(x=ct2.index, y=ct2[col], name=col[0] + ", " + data.iloc[col[1]]["Indicator Name"], legendgroup=col[0])
    
        fig2.update_layout(
            title="Indicator Comapison Plot",
            xaxis_title="Year",
            yaxis_title="Value",
            showlegend=enableLegend,
            hovermode="x",
            plot_bgcolor="White",
            hoverlabel={'bgcolor':"#f9f9f9", 'bordercolor':"black", 'namelength':-1}
        )

        return fig2

local_css("style.css")

data = pd.read_csv("WDIData.csv")

st.sidebar.title("Navigation")
pages = ["About the Dataset","Interactive Plots","Interesting Insights"]
page = st.sidebar.radio("Go To",pages,index=1)

if page=='Interactive Plots':
    st.write(
    """ 
    # Interactive Plots for World Development Indicators

    Produce plots for various indicators
    and for various countries.
    """
    )

    col1, col2 = st.beta_columns(2)

    with col1:
        use = st.beta_expander("How to use",False)
        use.write(
            """
            **Choose countries**: 
            Select the countries that you want to comapare. (Default is "India","United States")
        
            **Enter minimum percentage of Data Present**: 
            There are indicators which do not have all the values present in the dataset. So there is a 'Data Present in %' column
            in the dataset which gives the percentage of values present for that particular indicator. You have to type in a number 
            (from 1 to 100) which will fetch indicators having value present for more than that number.
            (Default is "98")

            **Choose Indicators**:
            Select the indicators that you want to compare. (No Default)
        
            """
        )
    with col2:
        tips = st.beta_expander("Tips to use",False)
        tips.write(
            """
            * Countries that are bigger in size have more data values present for indicators.
            * Very few indicators have 100% or 99% data present. But many indicators have more than 98% data present.
            * You can zoom into the plot by clicking and dragging the cursor.
            * By enabling the legend, you can isolate lines in plots by clicking on a particular legend. But the size of the plot decreases.

            """
        )


    st.write("---")

    with st.beta_expander("Advanced Settings",False):
        adv1, adv2, adv3, adv4 = st.beta_columns([4,1,2,1])

        with adv1:
            datapresent = st.text_input("Enter minimum percentage of Data Present","98")

        with adv2:
            pass
        
        with adv4:
            pass

        with adv3:
            st.write("")
            st.write("")
            enableLegend = st.checkbox("Show Legend")

    st.write("---")
    
    country_list = st.multiselect(
        "Choose Countries/Categories", data["Country Name"].unique().tolist(), ["India", "United States"]
    )

    indicator_list = st.multiselect(
    "Choose Indicators", getIndicatorList(country_list,datapresent)
    )

    if indicator_list:
        st.plotly_chart(getCountryComparisonPlot(country_list,indicator_list,enableLegend))

    st.write("---")

    with st.beta_expander("Submit an Insight"):
        st.text("Your current plot will be saved for reference")
        name = st.text_input("Enter your name")
        ta = st.text_area("Enter Insight")

        if st.button("Submit"):
            if ta and name and indicator_list:
                st.success("Insight successfully submitted!")
            else:
                st.error("Please fill all fields!")
        
        st.markdown(
            """ **Note**: 
                Once you submit an insight, it will be sent for review. 
                If your insight is deemed interesting by the Admin, it will be posted on the 'Interesting Insights' page. 
            """
        )


if page=='About the Dataset':
    st.write(
        """
        # About the dataset
        
        The primary World Bank collection of development indicators, compiled from officially-recognized international sources. 
        It presents the most current and accurate global development data available, and includes national, regional and global estimates.
        
        Topics: Agriculture and Food Security, Climate Change, Economic Growth, 
        Education, Energy and Extractives, 
        Environment and Natural Resources, Financial Sector Development, 
        Gender, Health, Nutrition and Population, Macroeconomic Vulnerability and Debt, Poverty, 
        Private Sector Development, Public Sector Management, 
        Social Development, Social Protection and Labor, Trade, Urban Development
        
        Type: Time Series
        
        Periodicity: Annual
        
        Temporal Coverage: 1960 - 2020

        ---

        ### Take a look at the dataset here: 

        """
    )

    country_list2 = st.multiselect(
        "Choose Countries/Categories", data["Country Name"].unique().tolist()
    )
    if country_list2:
        st.dataframe(getCountryTable(country_list2))
        st.text("Tip: Click on the column names to sort values")






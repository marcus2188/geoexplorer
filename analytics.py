# IMPORT ALL NECESSARY MODULES
import string
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import folium as fl
import webbrowser as wb

def removeAllNullValues(somedf: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """ Drops all rows and columns with null value present in any data row cells """
    somedf.dropna(axis = 0, inplace = True)
    somedf.dropna(axis = 1, inplace = True)
    return somedf

def displayMultiLineGraphs(xdata: List, ydata: List[List], legenddata: List, figsize: tuple, labelfontsize: int, title: string, xlabel: string, ylabel: string, ):
    """ Plots a matplotlib multi line graphs of all the data"""
    graphdotcolours = ["red", "green", "blue", "orange", "yellow"]
    graphmarkers = ['o']
    plt.figure(figsize=figsize)
    for ind, cc in enumerate(legenddata):
        plt.plot(xdata, ydata[ind], color = graphdotcolours[ind], marker = graphmarkers[0], label = cc)
    plt.title(title, fontsize=labelfontsize)
    plt.xlabel(xlabel, fontsize=labelfontsize)
    plt.ylabel(ylabel, fontsize=labelfontsize)
    plt.legend(loc="upper left")
    plt.show()

def plotPopulationComparison(worldpop_df: pd.core.frame.DataFrame, country_name_list: List):
    """ Sets up to compare population trend amongst countries """
    country_name_list.sort()
    onlypop_df = worldpop_df[["Country", "1970 Population",  "1980 Population",  "1990 Population",  "2000 Population",  "2010 Population", "2015 Population", "2020 Population", "2022 Population"]]
    filteredcountrypop = onlypop_df[onlypop_df.Country.isin(country_name_list)]
    yearlist = [cc[:4] for cc in filteredcountrypop.columns.values.tolist()[1:]]
    countrypoparray = (filteredcountrypop.iloc[:, 1:]).to_numpy()
    displayMultiLineGraphs(yearlist, countrypoparray, country_name_list, (10, 7), 14, "Population Across The Years", "Year", "People")


def plotPopulationComposition(worldpop_df: pd.core.frame.DataFrame):
    """ Sets up to see how world population is shared in composition amongst countries"""
    pop_percentage = worldpop_df[["Country", "World Population Percentage"]]
    
    # Combine all countries less than X% share into a single row dubbed 'Others'
    threshold_percentage = 1.1
    pop_percentage_lessthanx = pop_percentage.loc[pop_percentage["World Population Percentage"]<threshold_percentage]
    pop_percentage_withoutx = pop_percentage.loc[pop_percentage["World Population Percentage"]>=threshold_percentage]
    new_row = {"Country": "Others", "World Population Percentage": pop_percentage_lessthanx["World Population Percentage"].sum()}
    reformed_df = pd.concat([pop_percentage_withoutx, pd.DataFrame([new_row])], axis=0, ignore_index=True)
    explodelist = [d/(2*reformed_df["World Population Percentage"].sum()) for d in reformed_df["World Population Percentage"].tolist()]
    plt.pie(reformed_df["World Population Percentage"].tolist(), labels=reformed_df["Country"].tolist(), colors=sb.color_palette('bright'), autopct='%.0f%%', textprops={'fontsize': 7}, explode=explodelist, rotatelabels=True)
    plt.show()

def plotGeoDensity(worldpop_df: pd.core.frame.DataFrame):
    """ Visualize the density of each country on a big world map """
    countrydensityonly = worldpop_df[["Country", "Density"]]
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    country_shapes = f'{url}/world-countries.json'
    countrydensityonly.replace('United States', "United States of America", inplace = True) 
    countrydensityonly.replace("Republic of the Congo", "Democratic Republic of the Congo", inplace = True)
    countrydensityonly.replace("Serbia", "Republic of Serbia", inplace = True)
    countrydensityonly.replace("Tanzania", "United Republic of Tanzania", inplace = True)
    countrydensityonly.drop(countrydensityonly[countrydensityonly["Density"]>800].index, inplace = True)
    worldmap = fl.Map()
    fl.Choropleth(geo_data=country_shapes, name="Choropleth Density", data=countrydensityonly, columns=["Country", "Density"], bins=8 , key_on='feature.properties.name', fill_color='YlOrRd', nan_fill_color='black').add_to(worldmap)
    worldmap.save("diagrams/densityworldmap.html")

if __name__ == '__main__':
    # READ DATA FILES
    worldpop_df = pd.read_csv("datasets/worldpopulation.csv")
    worldpop_nonnull = removeAllNullValues(worldpop_df)

    # PLOT POPULATION TREND OF RANDOM 4 COUNTRIES IN CONSOLE
    countrynames = ["China", "United States", "United Kingdom", "India"]
    # plotPopulationComparison(worldpop_nonnull, countrynames)

    # PLOT PIECHART OF POPULATION SHARE
    # plotPopulationComposition(worldpop_nonnull)

    # VISUALIZE COUNTRY DENSITY ON A MAP
    plotGeoDensity(worldpop_nonnull)
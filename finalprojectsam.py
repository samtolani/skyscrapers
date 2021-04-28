import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk

def read_data(fileName):
    df = pd.read_csv(fileName)
    lst = []

    columns = ['Name', 'Main use', 'Country', 'City', 'Lat', 'Lon']

    for index, row in df.iterrows():
        sub = []
        for col in columns:
            index_no = df.columns.get_loc(col)
            sub.append(row[index_no])
        lst.append(sub)

    return lst


def countries_list(data):
    countries = []

    for i in range(len(data)):
        if data[i][2] not in countries:
            countries.append(data[i][2])

    return countries

def freq_data(data, countries, City):
    freq_data = {}

    for Country in countries:
        freq = 0
        for i in range(len(data)):
            if data[i][2] == Country and City >= data[i][4]:
                freq += 1
        freq_dict[Country] = freq

    return freq_dict

def bar_chart(freq_dict):
    x = freq_dict.keys()
    y = freq_dict.values()

    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('Countries')
    plt.ylabel('Frequencies of Listings')
    title = 'Listing in'
    for key in freq_dict.keys():
        title += ' ' + key
    plt.title(title)

    return plt

def display_map(data, countries, city):
    loc = []
    for i in range(len(data)):
        if data[i][1] in countries and city >= data [i][4]:
            loc.append([data[i][0], data[i][2], data[i][3]])

    map_df = pd.DataFrame(loc, columns=['Listing', 'lat', 'lon'])

    view_state = pdk.ViewState(latitude=map_df['lat'].mean(), longitude=map_df['lon'].mean(), zoom=10, pitch=0)
    layer = pdk.Layer('ScatterplotLayer', data=map_df, get_position='[lon,lat]', get_radius=150, get_color=[0, 255, 255], pickable = True)
    tool_tip = {'html': 'Listing:<br/>{Listing}', 'style:': {'backgroundColor': 'steelblue', 'color': 'white'}}

    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-b9', initial_view_state=view_state, layers=[layer], tooltip=tool_tip)

    st.pydeck_chart(map)

def main():
    data = read_data('skyscrapers.csv')

    st.title('Skyscrapers Web Application')
    st.write('Welcome!')

    countries = st.sidebar.multiselect('Select Countries', countries_list(data))
    CityLimit = st.sidebar.slider('Set City Limit', 10, 15, 20)

    if len(countries)> 0:
        st.write('Map of Countries')
        display_map(data, countries, CityLimit)
        st.write('\nCount of Countries')
        st.pyplot(bar_chart(freq_data(data, countries, CityLimit)))

    main()


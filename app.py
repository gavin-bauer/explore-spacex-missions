from my_modules import *
import requests
from bs4 import BeautifulSoup 
from io import BytesIO
from PIL import Image
import json
import math
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import streamlit as  st
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn')
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams['axes.labelsize'] = 9
plt.rcParams['axes.titlesize'] = 15
plt.rcParams['legend.fontsize'] = 10

def main():
    # LOAD DATA
    data_url = ('https://api.spacexdata.com/v3/launches')
    data, landings, payloads = load_data(data_url)

    # HEADER
    st.title('SpaceX Dashboard 🚀')

    # SIDEBAR
    st.sidebar.markdown('''
    ### THE APP by [Gavin Bauer](https://www.linkedin.com/in/gavinbauer/)
    This web app explores SpaceX's mission data from Launches, Payloads, Landings and Reuse.
    ''')

    app_mode = st.sidebar.selectbox("Choose a section", ["💽 Raw Mission Data", "🚀 Launches", "🛰️ Payloads", "🧳 Landings", "♻️ Reuse"])

    st.sidebar.markdown('''
    ### ABOUT
    This site was created for educational purposes only and is not affiliated with SpaceX.
    ''')

    st.sidebar.markdown('''
    ### CREDITS
    * [SpaceX](https://www.spacex.com/) for its media
    * [Wikipedia](https://www.wikipedia.org/) for its infobox
    * [R-SpaceX](https://github.com/r-spacex/SpaceX-API) for its REST API
    ''')

    st.sidebar.markdown('''
    ### FOLLOW THE AUTHOR
    [LinkedIn](https://www.linkedin.com/in/gavinbauer/) | [GitHub](https://github.com/raimanu) | [Twitter](https://twitter.com/gavinrbauer)
    ''')

    # DATASET
    if app_mode == '💽 Raw Mission Data':
        number_of_launches = str(landings.shape[0]) # choose landings instead of data to exclude scheduled launches
        st.markdown('### RAW MISSION DATA''')
        st.write(f"The mission data covers a wide range of information about SpaceX's {number_of_launches} launches ranging from Rockets, Payloads, Cores, Landpads...")
        st.write(data)

    # LAUNCHES
    if app_mode == '🚀 Launches':
        # introduction
        st.markdown('### LAUNCHES HISTORY')
        number_of_launches = str(data[data['launch_success'] == True].shape[0])
        st.write(f"As of today, SpaceX has successfully launched {number_of_launches} rockets. Designed and operated by SpaceX, the rocket fleet includes: Falcon 9, Falcon Heavy, Falcon 1.")
        rockets_img = st.checkbox("Tick box to view fleet")
        if rockets_img:
            st.image('img/rockets.PNG', caption="credits: [SpaceX Mission Watch(spacexmissionwatch.com)]", use_column_width=True)

        rocket = st.selectbox('Select a Rocket to view its launch history', sorted(data['rocket.rocket_name'].unique()))

        cols = ['launch_year', 'launch_success_or_failure']
        ylabel = 'Number of launches'

        if rocket == 'Falcon 1':
            # plot
            df = data[data['rocket.rocket_name'] == 'Falcon 1']
            title = f"{rocket}'s Launches History"
            st.pyplot(stacked_bar(df, cols, ylabel, title))
            # about rocket
            falcon_1 = st.checkbox("Learn more about Falcon 1")
            if falcon_1:
                WIKI_URL = 'https://en.wikipedia.org/wiki/Falcon_1'
                st.write(scrape_wikipedia_table(WIKI_URL))
                st.markdown('*Source: [Wikipedia](https://en.wikipedia.org/wiki/Falcon_1)*')

        elif rocket == 'Falcon Heavy':
            # plot
            df = data[data['rocket.rocket_name'] == 'Falcon Heavy']
            title = f"{rocket}'s Launches History"
            st.pyplot(stacked_bar(df, cols, ylabel, title))
            # about rocket
            falcon_heavy = st.checkbox("Learn more about Falcon Heavy")
            if falcon_heavy:
                WIKI_URL = 'https://en.wikipedia.org/wiki/Falcon_Heavy'
                st.write(scrape_wikipedia_table(WIKI_URL))
                st.markdown('*Source: [Wikipedia](https://en.wikipedia.org/wiki/Falcon_Heavy)*')

        elif rocket == 'Falcon 9':
            # plot
            df = data[data['rocket.rocket_name'] == 'Falcon 9']
            title = f"{rocket}'s Launches History"
            st.pyplot(stacked_bar(df, cols, ylabel, title))
            # about rocket
            falcon_heavy = st.checkbox("Learn more about Falcon 9")
            if falcon_heavy:
                WIKI_URL = 'https://en.wikipedia.org/wiki/Falcon_9'
                st.write(scrape_wikipedia_table(WIKI_URL))
                st.markdown('*Source: [Wikipedia](https://en.wikipedia.org/wiki/Falcon_9)*')

        # else: rocket == 'all'

    # PAYLOADS
    if app_mode == '🛰️ Payloads':
        st.markdown('### PAYLOADS HISTORY')
        sum_payloads = np.round(payloads['payload_mass_kg'].sum())
        st.write(f"SpaceX has launched a total of {sum_payloads} kilograms worth of payloads into a variety of orbits. The payloads' weight can range from the smallest cubesats of 1 kilogram, to comsats over 5 tonnes. With Falcon 9 and Falcon Heavy, SpaceX is able to cover most mission types.")
        cols = ['launch_year', 'orbit', 'payload_mass_kg']
        st.pyplot(stacked_payloads(payloads, cols))
        st.markdown('*VLEO = Very Low Earth Orbit, GTO = Geostationary Transfer Orbit, PO = Polar Orbit, ISS = International Space Station*')
        orbits = st.checkbox('View list of orbits')
        if orbits:
            st.image('https://www.airports-worldwide.com/img/articles/article0240_picture01.png', caption='List of Orbits', use_column_width=True)

    # LANDINGS
    if app_mode == '🧳 Landings':
        """
        ### LANDINGS HISTORY
        After launch, most rockets are designed to burn up on re-entry. On the other hand, SpaceX rockets are designed not only to withstand re-entry, but also to return to the launch pad for a vertical landing -- an incredibly difficult task, though almost routine nowadays.
        """
        cols = ['launch_year', 'landing_type']
        ylabel = 'Number of landings'
        title = 'Landings History by Platform'
        st.pyplot(stacked_bar(landings, cols, ylabel, title))
        st.markdown('*ASDS = Autonomous Spaceport Drone Ship, RTLS = Return To Launch Site*')
        video = st.checkbox("Click here to watch Falcon's 9 first historic landing")
        if video:
            st.video("https://www.youtube.com/embed/1B6oiLNyKKI?start=6")

    # REUSE
    if app_mode == '♻️ Reuse':
        """
        ### VEHICULE REFLOWN HISTORY
        Most rockets burn up upon re-entry, inducing a large cost. SpaceX rockets, on the other hand, are designed to withstand re-entry, but also return to the launchpad. As a result, SpaceX is able to substantially reduce the cost of space access by reusing the space vehicule.
        """
        cols = ['launch_year', 'reflown_or_first_flight']
        ylabel = 'Number of launches'
        title = 'Rocket Reuse History'
        st.pyplot(stacked_bar(landings, cols, ylabel, title))

if __name__ == '__main__':
    main()

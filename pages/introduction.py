import streamlit as st
from st_pages import show_pages_from_config, add_page_title

add_page_title()

show_pages_from_config()

st.write("""
        ## About
        "Immigrati.Stat" is a comprehensive data warehouse developed by Istat, focusing on the statistical data about foreign immigrants and new citizens in Italy. It aims to streamline access to various statistics for a wide array of users including researchers, policymakers, journalists, and citizens.
         
         The "Immigrati.Stat" project was initiated on 22nd July 2012 with a mission to collate and organize diverse statistics related to foreign immigrants in Italy, offering a holistic view of the phenomenon. It encompasses several key areas such as population, health, labor, education, economic conditions, social security, welfare, social participation, and crime.
        """
)

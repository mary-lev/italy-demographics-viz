import streamlit as st
from st_pages import show_pages_from_config, add_page_title

add_page_title()

show_pages_from_config()

st.write("""
        ## Original dataset and mushup datasets
         Some text here
         
        ## Quality analysis of the datasets
         
        ## Legal analysis (privacy, license, purpose, etc.)
         
        ## Ethics anlysis
        
        ## Technical analysis (formats, metadati, URI, provenance)
        
        ## Sostenibility of the update the datasets over the time
        """
)

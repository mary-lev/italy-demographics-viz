import streamlit as st

st.set_page_config(
    page_title = "Dataset Analysis",
    page_icon = ":file_cabinet:",
)

st.write("""
        ## Original dataset and mushup datasets
        The datasets are characterized by their high-quality standards, following the technical specifications of WCAG 2.0. 
        However, it’s noted that the site currently does not conform to all the accessibility standards outlined 
         in EU Decision 2018/1523.
         
        ## Quality analysis of the datasets
        The data within Immigrants.Stat are presented in multidimensional tables, allowing for a high degree of customization 
         and analysis. The use of standard metadata ensures ease of access and understanding for users.
         
        ## Legal analysis (privacy, license, purpose, etc.)
        The platform is openly accessible to the public and free of charge, reflecting its compliance with open 
         data principles and ensuring broad usability.
         
        ## Ethics anlysis
        
        ## Technical analysis (formats, metadati, URI, provenance)
        The data warehouse employs OECD.Stat technology, similar to the I.Stat platform used by Istat. 
         This technology allows for advanced data organization, retrieval, and analysis.
        
        ## Sostenibility of the update the datasets over the time
        The ongoing development of Immigrants.Stat implies a commitment to continuous updates and additions, 
         ensuring the platform remains relevant and reflective of current trends and data.
        """
)

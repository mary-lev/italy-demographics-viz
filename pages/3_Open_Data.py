import streamlit as st

st.set_page_config(
    page_title = "LOD",
    page_icon = ":linked_paperclips:"
)

st.title("Metadata for STRASA 2022 Provincial Data: Resident Foreigners")

st.write("""
        ### 1. Dataset Overview
        Dataset Name: Resident Foreigners on 1st January 2022 by Age and Sex
        Description: This dataset provides demographic information about the foreign resident population in various Italian provinces as of 1st January 2022, detailing age and gender distribution.
        Format: CSV (Comma-Separated Values)
        Data Collection Period: As of 1st January 2022
        Source: Italian National Institute of Statistics (Istat)

        ### 2. Column Descriptions

        Province_Code: The code assigned to each province for identification purposes.
        Province: The name of the province.
        Age: Age of the individuals (likely categorized in groups or as a specific age).
        Males: Number of male foreign residents in the province.
        Females: Number of female foreign residents in the province.

        ### 3. Data Quality and Limitations

        Data accuracy is subject to Istat's reporting standards.
        Age categorization method not specified (individual years, groups, or ranges).
        Data specific to foreign residents only; does not include local citizens.

        ### 4. Usage Rights and Licensing

        Open for public use, subject to Istat's data distribution policies.

        ### 5. Update Frequency

        Annually

        ### 6. Accessibility and Format

        Accessible for download in CSV format.

        ### 7. Contact Information

        For inquiries and further information, contact michele.camisasca@istat.it.

        ### 8. Technical Requirements

        Compatible with standard data analysis software capable of processing CSV files.

        ### 9. Supplementary Materials

        None specified.

        ### 10. Additional Notes

        Ideal for demographic studies, migration research, social policy analysis, and resource allocation planning for foreign residents.
        """
)

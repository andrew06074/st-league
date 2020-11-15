import streamlit as st
import awesome_streamlit as ast

import numpy as np
import pandas as pd

import src.team
import src.overview

PAGES = {
    "Overview": src.overview,
    "Team": src.team
    
}

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("My view scope",list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection}..."):
        ast.shared.components.write_page(page)


if __name__ == "__main__":
    main()
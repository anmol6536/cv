import streamlit as st


def width_change(pct: int):
    """
    Change the width of the main content area
    :param pct: int
    :return: None
    """
    css = f'''
    <style>
        section.main > div {{max-width:{pct}rem}}
        [data-testid="stExpander"] div:has(>.streamlit-expanderContent) {{
            overflow: scroll;
            height: 400px;
        }}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)
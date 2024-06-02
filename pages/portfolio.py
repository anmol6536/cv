from utilities.globals import GlobalPaths
import streamlit as st
from pages.home_page import image_carousel


def portfolio():
    IMAGE_FOLDER = GlobalPaths.IMAGE_FOLDER / "photography"
    sub_folders = [i for i in IMAGE_FOLDER.iterdir() if i.is_dir()]
    for folder in sub_folders:
        st.markdown(f"## {folder.stem}")
        image_carousel(folder)
        st.divider()


portfolio()

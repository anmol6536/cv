from pages.home_page import recent_publications, title_card, experience, contact_user, image_carousel, github_showcase
from utilities.custom_steamlit_fuctions import width_change
import streamlit as st

width_change(80)

# https://myaccount.google.com/apppasswords


def main():
    contact_user()

    title_card()
    recent_publications()
    experience()

    st.title("Hobbies")
    # PHOTOGRAPHY
    st.subheader("Photography")
    image_carousel()
    if st.button("More Photos", use_container_width=True):
        st.switch_page("pages/portfolio.py")

    github_showcase()


if __name__ == '__main__':
    main()

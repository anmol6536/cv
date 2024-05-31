from pages.home_page import recent_publications, title_card, experience, contact_user
from utilities.custom_steamlit_fuctions import width_change

width_change(80)
# https://myaccount.google.com/apppasswords

def main():
    title_card()
    recent_publications()
    experience()
    contact_user()

if __name__ == '__main__':
    main()

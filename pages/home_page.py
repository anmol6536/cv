from __future__ import absolute_import

from datetime import datetime
from typing import Any, Optional

import streamlit as st

from utilities.generic_utilities import yielder
from utilities.globals import GlobalPaths
from utilities.yaml_handler import get_yaml_attribute


def title_card():
    YAML = GlobalPaths.TEXT_YAML
    name = get_yaml_attribute(YAML, lambda x: x.get("personal_info").get("name"))
    short_bio = get_yaml_attribute(YAML, lambda x: x.get("personal_info").get("short_bio"))
    st.title(name)

    # create 2 columns with 1:3 ratio
    left, right = st.columns([1, 3])
    left.image(str(GlobalPaths.IMAGE_FOLDER / "profile_pic.jpg"), use_column_width=True)
    right.markdown(short_bio)
    right.divider()
    with right:
        n = 8
        values = get_yaml_attribute(YAML, lambda x: x.get("personal_info").get("profile_urls"))
        for dictionaries in yielder(values, n):
            columns = st.columns(n)
            for c, dictionary in zip(columns, dictionaries):
                with c:
                    (item, value), *_ = dictionary.items()
                    st.markdown(f"[{item}]({value})", unsafe_allow_html=True)
    st.divider()


def recent_publications():
    YAML = GlobalPaths.TEXT_YAML
    publications = get_yaml_attribute(YAML, "recent_publications")
    st.markdown("## Recent Publications")
    for data in yielder(publications, 3):
        if len(data) == 3:
            ldata, cdata, rdata = data
        if len(data) == 2:
            ldata, cdata = data
            rdata = None
        if len(data) == 1:
            ldata = data[0]
            cdata = rdata = None
        left, center, right = st.columns(3)
        publication_card(ldata, left)
        publication_card(cdata, center)
        publication_card(rdata, right)
    st.divider()


def publication_card(data: Optional[dict[str, Any]], column: st.columns) -> None:
    if data is None:
        return
    with column:
        with st.expander(data.get("title")):
            st.markdown(f"> {data.get('year')} | {data.get('journal')}")
            st.markdown(data.get("authors"))


def experience():
    YAML = GlobalPaths.TEXT_YAML
    full_time_data = get_yaml_attribute(YAML, lambda x: x.get("professional_journey").get("full_time"))
    full_time_data = sorted(full_time_data, key=lambda x: datetime.fromisoformat(x.get('start')), reverse=True)
    st.write("## Experience")
    for data in full_time_data:
        experience_card(data)
    st.divider()


def experience_card(data: Optional[dict[str, Any]]) -> None:
    with st.expander("", expanded=True):
        st.markdown(f"#### {data.get('title')} | {data.get('institution')}")
        start, end = data.get("start"), data.get("end")
        if end.lower() == "present":
            end = datetime.now()
            present = True
        else:
            end = datetime.fromisoformat(end)
            present = False
        start = datetime.fromisoformat(start)
        delta = (end - start).days / 364.25
        st.markdown(f"Experience: {round(delta, 2)} years {'(Present)' if present is True else ''}")

        st.divider()
        abstract = data.get("abstract")
        if isinstance(abstract, str):
            st.write(abstract)
        elif isinstance(abstract, list):
            for item in abstract:
                st.write(f"- {item}")


def contact_user():
    with st.form("ContactForm"):
        first_name_column, last_name_column = st.columns(2)
        first_name_column.text_input("First Name", key='first_name')
        last_name_column.text_input("Last Name", key='last_name')
        your_email = st.text_input("Your Email Address", key="user_email")
        st.text_area("Message", key='contact_message')
        submit_button = st.form_submit_button("Send Message", use_container_width=True)
        if submit_button is True:
            send_message()


def send_message():
    first_name = st.session_state.get("first_name")
    last_name = st.session_state.get("last_name")

    import yagmail
    from uuid import uuid4
    from copy import deepcopy

    yag = yagmail.SMTP(st.secrets.get('contact_mail').get("email_address"),
                       st.secrets.get('contact_mail').get("email_password"))
    replace_this = f"{first_name} {last_name} tried to contact you"
    contents = [
        "{replace_this}",
        "",
        f"User E-Mail: {st.session_state.get('user_email')}",
        "Message:",
        st.session_state.get("contact_message")
    ]
    contents = "\n".join(iter(contents))
    ticket_id = uuid4()
    subject = f'Message from HOMEWEBSITE ({ticket_id})'

    yag.send(st.secrets.get('contact_mail').get("email_address"),
             subject,
             deepcopy(contents).format(replace_this=replace_this))

    replace_this = "You tried to contact Anmol Gorakshakar"
    yag.send(st.session_state.get('user_email'),
             subject,
             "REFERENCE:\n" + deepcopy(contents).format(replace_this=replace_this))
    del contents
    st.info("Message Sent")

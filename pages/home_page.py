from __future__ import absolute_import

from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union
from itertools import zip_longest
from re import sub

import streamlit as st

from utilities.generic_utilities import yielder
from utilities.globals import GlobalPaths
from utilities.yaml_handler import get_yaml_attribute
from src.github_api import get_public_github_data
from src.generic_badge import generic_shield
from copy import deepcopy


def title_card():
    YAML = GlobalPaths.TEXT_YAML
    name = get_yaml_attribute(YAML, lambda x: x.get("personal_info").get("name"))
    short_bio = get_yaml_attribute(YAML, lambda x: x.get("personal_info").get("short_bio"))
    st.title(name)

    # create 2 columns with 1:3 ratio
    left, right = st.columns([1, 3])
    left.image(str(GlobalPaths.IMAGE_FOLDER / "profile_pic.png"), use_column_width=True)
    right.markdown(short_bio)
    right.divider()
    with right:
        profile_urls = get_yaml_attribute(YAML, lambda x: x.get("personal_info").get("profile_urls"))
        BASE_IMAGE_MARKDOWN = """<a href={href} target="_blank"><img src="{src}"></a>"""
        render_string = ""
        for dictionary in profile_urls:
            render_string += deepcopy(BASE_IMAGE_MARKDOWN).format(href=dictionary.get("user_url"),
                                                                  src=dictionary.get("logo_url")) + "\t\t"
        st.markdown(render_string, unsafe_allow_html=True)
    st.divider()


def recent_publications():
    YAML = GlobalPaths.TEXT_YAML
    publications = get_yaml_attribute(YAML, "recent_publications")
    st.title("Recent Publications")
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
            st.link_button("Full Article", data.get("url"), use_container_width=True)


def experience():
    YAML = GlobalPaths.TEXT_YAML
    full_time_data = get_yaml_attribute(YAML, lambda x: x.get("professional_journey").get("full_time"))
    full_time_data = sorted(full_time_data, key=lambda x: datetime.fromisoformat(x.get('start')), reverse=True)
    st.title("Experience")
    for data in full_time_data:
        experience_card(data)


def experience_card(data: Optional[dict[str, Any]]) -> None:
    with st.container(border=False):
        st.subheader(f"{data.get('title')} | {data.get('institution')}")
        start, end = data.get("start"), data.get("end")
        if end.lower() == "present":
            end = datetime.now()
            present = True
        else:
            end = datetime.fromisoformat(end)
            present = False
        start = datetime.fromisoformat(start)
        delta = (end - start).days / 364.25
        st.markdown(f"> Experience: {round(delta, 2)} years {'(Present)' if present is True else ''}")

        abstract = data.get("abstract")
        if isinstance(abstract, str):
            st.write(abstract)
        elif isinstance(abstract, list):
            for item in abstract:
                st.write(f"- {item}")
        st.divider()


def contact_user():
    with (st.sidebar.form("ContactForm")):
        st.write("Contact Me")
        if st.session_state.get("submitted") is True:
            send_message()
        first_name_column, last_name_column = st.columns(2)
        first_name_column.text_input("First Name", key='first_name')
        last_name_column.text_input("Last Name", key='last_name')
        st.text_input("Your Email Address", key="user_email")
        st.text_area("Message", key='contact_message')
        st.form_submit_button("Send Message", use_container_width=True, on_click=send_message)


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
    subject = f'Message from CV Website ({ticket_id})'

    yag.send(st.secrets.get('contact_mail').get("email_address"),
             subject,
             deepcopy(contents).format(replace_this=replace_this))

    subject = f'Thank you for contacting Anmol Gorakshakar (ID: {ticket_id})'
    replace_this = "You tried to contact Anmol Gorakshakar"
    if st.session_state.get('user_email', None) is not None:
        yag.send(st.session_state.get('user_email'),
                 subject,
                 "REFERENCE:\n" + deepcopy(contents).format(replace_this=replace_this))
    del contents

    # reset form
    st.session_state["user_email"] = None
    st.session_state["first_name"] = None
    st.session_state["last_name"] = None
    st.session_state["contact_message"] = None
    st.sidebar.info("Message Sent")

# ----------------------------------------------------------------------------------------------------------------------

def image_height(path: Union[str, Path]) -> float:
    from PIL import Image
    w, h = Image.open(path).size
    return h / w


def image_carousel(image_folder: Path = None, top_n: int = None):

    IMAGES = list((image_folder or (GlobalPaths.IMAGE_FOLDER / "photography")).glob("*.jpg"))
    if top_n is not None:
        IMAGES = IMAGES[:top_n]
    with st.container(height=600, border=False):
        n = 4
        columns = st.columns(n)
        height_tracker = {col: 0 for col in columns}
        for image in IMAGES:
            if not image.is_file():
                continue
            col = image_column_assigner_v2(height_tracker)
            col.image(image.__str__())
            height_tracker[col] += image_height(image)


def image_column_assigner_v2(column_height_dictionary: dict[str, int]) -> st.columns:
    (column, _), *_ = sorted(column_height_dictionary.items(), key=lambda x: x[1])
    return column

# ----------------------------------------------------------------------------------------------------------------------


def github_showcase():
    from json import loads
    data = loads(GlobalPaths.GITHUB_SHOWCASE_JSON.read_text())
    st.title("Github Showcase")
    n = 3
    columns = st.columns(n)
    for repos in yielder(data, n):
        for repo, col in zip_longest(repos, columns):
            if repo is None:
                continue
            github_repo_card(repo, col)


def github_repo_card(data: dict[str, Any], col: st.columns):
    with col:
        with st.expander(data.get("name")):
            name = sub(r"[^a-zA-Z0-9]", " ", data.get("name")).upper()
            hl_color = "yellow" if data.get("private") else "#00000000"
            private = f"<span style='background-color: {hl_color};'> {'Private' if data.get('private') else 'Public'}</span>"
            st.markdown(f"#### [{name}]({data.get('url')})")
            st.markdown(f"> Created At: {data.get('created_at')} | {private}", unsafe_allow_html=True)
            st.markdown(f"Size: {data.get('size')} KB")
            for shield in data.get('shield_logo'):
                st.image(generic_shield(shield, shield))
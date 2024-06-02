import streamlit as st
from requests import get
from io import BytesIO
from base64 import b64encode


def shield_maker_form():
    if (preset := st.session_state.get("shield_preset")) is not None:
        if preset == "Jira":
            st.session_state.__setattr__("shield_logo", "Jira")
            st.session_state.__setattr__("shield_logo_color", "white")
            st.session_state.__setattr__("shield_style", "for-the-badge")
            st.session_state.__setattr__("shield_background_color", '#0052CC')
            st.session_state.__setattr__("version_badge", False)
            label_text = "Jira Ticket"
        if preset == "Version":
            logo_options = logos()
            st.selectbox("Select Logo", options=logo_options.__dict__.keys(), index=0, key='shield_logo')
            st.session_state.__setattr__("shield_logo_color", "white")
            st.session_state.__setattr__("shield_style", "for-the-badge")
            st.session_state.__setattr__("shield_background_color", 'green')
            st.session_state.__setattr__("version_badge", True)
            label_text = "Version"
    else:
        preset = None
        label_text = "Label"
        st.session_state.__setattr__("version_badge", False)

    st.text_input(label_text,
                  value="testLabel", help="Text to create the label with", key='shield_label')

    st.selectbox("Select a Preset", options=[None, 'Jira', 'Version'], key="shield_preset")

    if preset is None:
        left_column, right_column = st.columns(2)

        logo_options = logos()
        left_column.selectbox("Select Logo", options=logo_options.__dict__.keys(), index=0, key='shield_logo')

        logo_color_column, bg_color_column = left_column.columns(2)
        logo_color_column.color_picker("Logo Color", value='#ffffff', key='shield_logo_color')
        bg_color_column.color_picker("Background Color", key='shield_background_color')

        right_column.selectbox("Pick Label Style", options=['for-the-badge', 'flat', 'plastic'], key='shield_style')

    st.button("Submit", on_click=compiler, use_container_width=True, type='primary')


def compiler():
    base = "https://img.shields.io/badge"
    data = sanitize_label(st.session_state.get("shield_label"))
    color = st.session_state.get("shield_background_color", "blue").replace("#", '')
    parameters = dict(
        logo=getattr(logos(), st.session_state.get("shield_logo")),
        logoColor=st.session_state.get("shield_logo_color", 'white').replace("#", ''),
        style=st.session_state.get('shield_style')
    )
    base = f"{base}/{data}-{color}.svg"

    URL = base + "?" + "&".join(f"{k}={v}" for k, v in parameters.items())

    st.code(URL)
    render_shield(URL)


def render_shield(url: str) -> None:
    # Fetch the URL and display the image
    response = get(url)
    if response.ok:
        svg_data = BytesIO(response.content).getvalue().decode('utf-8').encode()
        st.markdown(f'<img src="data:image/svg+xml;base64,{b64encode(svg_data).decode()}" alt="shield"/>', unsafe_allow_html=True)
        st.write("")
    else:
        st.error("Failed to fetch the shield image.")


def logos():
    from utilities.yaml_handler import get_yaml_attribute
    from utilities.globals import GlobalPaths

    YAML = GlobalPaths.SHIELD_YAML
    logos = get_yaml_attribute(YAML, "logos")

    return type('logos', (object,), {k: v for j in logos for k,v in j.items()})


def sanitize_label(label:str) -> str:
    if st.session_state.get("version_badge", False) == False:
        label = label.replace('-', '--')
    label = label.replace(' ', '_')
    label = label.replace('_', '__')
    return label

shield_maker_form()
def generic_shield(label, logo, background_color='black', logo_color='white', style='for-the-badge'):
    base = "https://img.shields.io/badge"
    base = f"{base}/{label}-{background_color}.svg"

    parameters = dict(
        logo=logo,
        logoColor=logo_color,
        style=style
    )
    return base + "?" + "&".join(f"{k}={v}" for k, v in parameters.items())

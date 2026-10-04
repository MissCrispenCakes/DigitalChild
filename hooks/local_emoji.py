"""Render bundled Material icons and Unicode emoji without remote images."""

from material.extensions import emoji as material_emoji
from pymdownx import emoji


def render_local(index, shortname, alias, uc, alt, title, category, options, md):
    """Keep local SVG icons; render ordinary emoji as browser-native text."""
    args = (index, shortname, alias, uc, alt, title, category, options, md)
    if uc:
        return emoji.to_alt(*args)
    return material_emoji.to_svg(*args)


def on_config(config):
    """Apply the generator after MkDocs has parsed extension configuration."""
    config.mdx_configs["pymdownx.emoji"]["emoji_generator"] = render_local
    return config

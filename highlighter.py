import html
from htbuilder import H, HtmlElement
from htbuilder.units import unit
from annotated_text import annotation
import annotated_text.parameters as p

# This works in 3.7+:
# from htbuilder import span
#
# ...so we use the 3.7 version of the code above here:
span = H.span

def highlight_words_in_text(text, words_to_highlight, background=None, color=None, **style):
    color_style = {}

    if color:
        color_style['color'] = color

    if background:
        background_color = background
    else:
        label_sum = sum(ord(c) for c in "highlight")
        background_color = p.PALETTE[label_sum % len(p.PALETTE)]
        background_opacity = p.OPACITIES[label_sum % len(p.OPACITIES)]
        background = background_color + background_opacity

    out = span()

    current_position = 0
    text_lower = text.lower()

    for word in words_to_highlight:
        word_lower = word.lower()
        index = text_lower.find(word_lower, current_position)

        if index != -1:
            # Add the text before the highlighted word
            out(html.escape(text[current_position:index]))

            # Add the highlighted word
            out(annotation(word, background=background, color=color, **style))

            # Update the current position
            current_position = index + len(word)

    # Add the remaining text after the last highlighted word
    out(html.escape(text[current_position:]))

    return out
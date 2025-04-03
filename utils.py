from PIL import Image
import streamlit as st
import os

CARD_DIR = "assets/cards"

def load_card_image(rank):
    """Load the image of a card by rank."""
    rank_map = {'J': '11', 'Q': '12', 'K': '13', 'A': '1'}
    rank = rank_map.get(rank, rank)
    image_path = os.path.join(CARD_DIR, f"{rank}.png")
    if os.path.exists(image_path):
        return Image.open(image_path)
    return None

def display_hand(cards, hidden=False):
    """Display a list of card images in a single row."""
    if not cards:
        return

    cols = st.columns(len(cards))
    for i, card in enumerate(cards):
        with cols[i]:
            if card == "back":
                st.image(os.path.join(CARD_DIR, "back.png"), width=100)
            else:
                rank = card if card == '10' else card[0]
                card_img = load_card_image(rank)
                if card_img:
                    st.image(card_img, width=100)
                else:
                    st.text(card)

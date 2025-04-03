import os
from PIL import Image
import streamlit as st
from typing import Optional

def load_card_image(card_rank: str) -> Optional[Image.Image]:
    """Load a card image from the assets directory."""
    try:
        assets_dir = os.path.join(os.path.dirname(__file__), "assets", "cards")
        # Map card ranks to image numbers
        rank_to_number = {
            'A': '1',
            '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
            '7': '7', '8': '8', '9': '9', '10': '10',
            'J': '11', 'Q': '12', 'K': '13'
        }
        
        if card_rank not in rank_to_number:
            st.error(f"Invalid card rank: {card_rank}")
            return None
            
        image_number = rank_to_number[card_rank]
        image_path = os.path.join(assets_dir, f"{image_number}.png")
        return Image.open(image_path)
    except Exception as e:
        st.error(f"Error loading card image: {e}")
        return None

def display_card(card_rank: str, width: int = 100) -> None:
    """Display a card image in the Streamlit UI."""
    image = load_card_image(card_rank)
    if image:
        st.image(image, width=width)

def display_hand(cards: str, width: int = 100) -> None:
    """Display multiple cards in a row."""
    if not cards or cards.isspace():
        st.write("No cards")
        return
        
    card_list = cards.split()
    if not card_list:
        st.write("No cards")
        return
        
    cols = st.columns(len(card_list))
    for i, card in enumerate(card_list):
        with cols[i]:
            display_card(card, width) 
import streamlit as st
from PIL import Image
import os
from blackjack import game

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

def load_card_image(rank):
    """Load card image from the cards directory"""
    try:
        # Convert face cards to numbers
        if rank == 'J':
            rank = '11'
        elif rank == 'Q':
            rank = '12'
        elif rank == 'K':
            rank = '13'
        elif rank == 'A':
            rank = '1'
            
        return Image.open(f"cards/{rank}.png")
    except:
        return None

def display_hand(cards, hidden=False):
    """Display a hand of cards"""
    if not cards:
        return
    
    # Create a single row with columns for each card
    cols = st.columns(len(cards))
    for i, card in enumerate(cards):
        with cols[i]:
            if card == "back":
                st.image("cards/back.png", width=100)
            else:
                # Get the rank from the card string
                # For '10', we need to use the full string
                # For other cards, use the first character
                rank = card if card == '10' else card[0]
                card_img = load_card_image(rank)
                if card_img:
                    st.image(card_img, width=100)
                else:
                    st.text(card)

# Streamlit UI
st.markdown("""
    <style>
    .game-button {
        width: 100%;
        padding: 20px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .hit-button {
        background-color: #ff4b4b;
        color: white;
    }
    .hit-button:hover {
        background-color: #ff3333;
    }
    .stand-button {
        background-color: #4CAF50;
        color: white;
    }
    .stand-button:hover {
        background-color: #45a049;
    }
    .new-game-button {
        background-color: #2196F3;
        color: white;
    }
    .new-game-button:hover {
        background-color: #1976D2;
    }
    .centered-title {
        text-align: center;
        font-size: 48px;
        margin-bottom: 30px;
    }
    .centered-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Centered title
st.markdown('<h1 class="centered-title">🎮 Blackjack</h1>', unsafe_allow_html=True)

# Display chip pool
st.sidebar.header("Chip Pool")
st.sidebar.write(f"💰 {game.state.chip_pool}")

# Betting controls
if not game.state.playing:
    bet_amount = st.sidebar.number_input(
        "Place your bet",
        min_value=1,
        max_value=game.state.chip_pool,
        value=1
    )
    if st.sidebar.button("Place Bet"):
        if game.make_bet(bet_amount):
            st.session_state.game_started = True
            game.deal_cards()
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid bet amount!")

# Game controls
st.markdown('<div class="centered-container">', unsafe_allow_html=True)

# Create three columns for the buttons with equal width
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if not game.state.playing and game.state.bet > 0:
        if st.button("🔄 New Game", key="new_game", use_container_width=True):
            game.deal_cards()
            st.session_state.game_started = True
            st.experimental_rerun()

with col2:
    if game.state.playing:
        if st.button("🎯 Hit", key="hit", use_container_width=True):
            game.hit()
            st.experimental_rerun()

with col3:
    if game.state.playing:
        if st.button("🛑 Stand", key="stand", use_container_width=True):
            game.stand()
            st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Display game state
game_state = game.get_game_state()

if game_state['player_hand']:
    st.header("Dealer's Hand")
    display_hand(game_state['dealer_hand'], hidden=game_state['playing'])
    
    st.header("Your Hand")
    display_hand(game_state['player_hand'])
    
    # Display scores
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Your Score: {game_state['player_score']}")
    with col2:
        if not game_state['playing']:
            st.write(f"Dealer's Score: {game_state['dealer_score']}")
    
    # Display result
    if game_state['result']:
        st.header(game_state['result']) 
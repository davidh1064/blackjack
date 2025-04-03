import streamlit as st
from blackjack import BlackjackGame
from utils import display_hand

# Initialize game in session state
if 'game' not in st.session_state:
    st.session_state['game'] = BlackjackGame()

game = st.session_state['game']

# Streamlit UI setup
st.set_page_config(page_title="Blackjack", layout="centered")

st.markdown("""
    <style>
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

st.markdown('<h1 class="centered-title">🎮 Blackjack</h1>', unsafe_allow_html=True)

# Sidebar: Chip Pool & Betting
st.sidebar.header("Chip Pool")
st.sidebar.write(f"💰 {game.state.chip_pool}")

if not game.state.playing:
    bet_amount = st.sidebar.number_input("Place your bet", min_value=1, max_value=game.state.chip_pool, value=1)
    if st.sidebar.button("Place Bet"):
        if game.make_bet(bet_amount):
            game.deal_cards()
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid bet amount!")

# Game Control Buttons
st.markdown('<div class="centered-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if not game.state.playing and game.state.bet > 0:
        if st.button("🔄 New Game"):
            game.deal_cards()
            st.experimental_rerun()

with col2:
    if game.state.playing:
        if st.button("🎯 Hit"):
            game.hit()
            st.experimental_rerun()

with col3:
    if game.state.playing:
        if st.button("🛑 Stand"):
            game.stand()
            st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Display Game State
game_state = game.get_game_state()

if game_state['player_hand']:
    st.header("Dealer's Hand")
    display_hand(game_state['dealer_hand'], hidden=game_state['playing'])

    st.header("Your Hand")
    display_hand(game_state['player_hand'])

    # Scores
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Your Score: {game_state['player_score']}")
    with col2:
        if not game_state['playing']:
            st.write(f"Dealer's Score: {game_state['dealer_score']}")

    # Result
    if game_state['result']:
        st.header(game_state['result'])

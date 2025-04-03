import streamlit as st
import logging
import os
from blackjack.game import BlackjackGame
from blackjack.models.game_state import GamePhase
from utils import display_hand

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'game' not in st.session_state:
    st.session_state.game = BlackjackGame()

def main():
    st.title("🎮 Blackjack")
    
    # Display player's money
    st.sidebar.metric("Your Money", f"${st.session_state.game.player_money}")
    
    # Get current game state
    state = st.session_state.game.get_state()
    
    # Display dealer's hand
    st.subheader("Dealer's Hand")
    display_hand(state["dealer_hand"])
    st.write(f"Value: {state['dealer_value']}")
    
    # Display player's hand
    st.subheader("Your Hand")
    display_hand(state["player_hand"])
    st.write(f"Value: {state['player_value']}")
    
    # Display game message if any
    if state["message"]:
        st.info(state["message"])
    
    # Game controls based on phase
    if state["phase"] == "waiting_for_bet":
        bet = st.number_input("Place your bet", min_value=1, max_value=state["player_money"], value=10)
        if st.button("Start Round"):
            try:
                st.session_state.game.start_new_round(bet)
                st.experimental_rerun()
            except ValueError as e:
                st.error(str(e))
    
    elif state["phase"] == "player_turn":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Hit"):
                st.session_state.game.hit()
                st.experimental_rerun()
        with col2:
            if st.button("Stand"):
                st.session_state.game.stand()
                st.experimental_rerun()
    
    elif state["phase"] == "round_over":
        if st.button("New Round"):
            st.session_state.game.phase = GamePhase.WAITING_FOR_BET
            st.session_state.game.message = ""  # Clear the message
            st.experimental_rerun()

if __name__ == "__main__":
    main() 
import random

class GameState:
	def __init__(self):
		self.playing = False
		self.chip_pool = 100
		self.bet = 0
		self.deck = None
		self.player_hand = None
		self.dealer_hand = None
		self.result = ""
		self.show_all_cards = False  # New flag to control card visibility

# Hearts, Diamonds, Clubs, Spades
suits = ('H','D','S','C')

# Possible Card Ranks
ranking = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')

# Point Val Dict (Dual existence of Ace is defined later)
card_val = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

class Card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def __str__(self):
		return self.rank  # Only return the rank since we're using the same image for all suits

	def grab_suit(self):
		return self.suit

	def grab_rank(self):
		return self.rank

	def draw(self):
		return self.__str__()

class Hand:
	def __init__(self):
		self.cards = []
		self.value = 0
		self.ace = False

	def __str__(self):
		return " ".join(card.__str__() for card in self.cards)

	def card_add(self, card):
		self.cards.append(card)
		if card.rank == 'A':
			self.ace = True
		self.value += card_val[card.rank]

	def calc_val(self):
		if self.ace and self.value < 12:
			return self.value + 10
		return self.value

	def get_visible_cards(self, hidden=False, show_all=False):
		"""Return all cards, with the second card hidden for dealer if game is in progress"""
		if not self.cards:
			return []
			
		if hidden and len(self.cards) > 1 and not show_all:
			# Show first card, hide second card
			return [self.cards[0].draw(), "back"]  # Return "back" for the hidden card
		return [card.draw() for card in self.cards]

	def get_all_cards(self):
		"""Return all cards without hiding any"""
		return [card.draw() for card in self.cards]

class Deck:
	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranking:
				self.deck.append(Card(suit, rank))

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		if len(self.deck) == 0:
			self.__init__()
			self.shuffle()
		return self.deck.pop()

	def __str__(self):
		return " ".join(card.__str__() for card in self.deck)

class BlackjackGame:
	def __init__(self):
		self.state = GameState()
		self.restart_phrase = "Place a bet to start a new round, or click New Game to restart entire game."

	def make_bet(self, bet_amount):
		"""Set the bet amount for the current round"""
		try:
			bet_amount = int(bet_amount)
			if 1 <= bet_amount <= self.state.chip_pool:
				self.state.bet = bet_amount
				return True
			return False
		except (ValueError, TypeError):
			return False

	def deal_cards(self):
		"""Deal initial cards to player and dealer"""
		self.state.deck = Deck()
		self.state.deck.shuffle()
		
		self.state.player_hand = Hand()
		self.state.dealer_hand = Hand()
		
		# Deal initial cards
		self.state.player_hand.card_add(self.state.deck.deal())
		self.state.player_hand.card_add(self.state.deck.deal())
		self.state.dealer_hand.card_add(self.state.deck.deal())
		self.state.dealer_hand.card_add(self.state.deck.deal())
		
		self.state.playing = True
		self.state.show_all_cards = False
		self.state.result = "Hit or Stand? Press the buttons above."
		return True

	def hit(self):
		"""Player takes another card"""
		if not self.state.playing:
			self.state.result = "Sorry, can't hit" + self.restart_phrase
			return False

		if self.state.player_hand.calc_val() <= 21:
			self.state.player_hand.card_add(self.state.deck.deal())
			
		if self.state.player_hand.calc_val() > 21:
			self.state.result = 'Busted!' + self.restart_phrase
			self.state.chip_pool -= self.state.bet
			self.state.playing = False
			self.state.show_all_cards = True
			return False
		return True

	def stand(self):
		"""Player stands, dealer plays their hand"""
		if not self.state.playing:
			self.state.result = "Sorry, you can't stand!"
			return False

		# Dealer draws until 17 or higher
		while self.state.dealer_hand.calc_val() < 17:
			self.state.dealer_hand.card_add(self.state.deck.deal())

		dealer_val = self.state.dealer_hand.calc_val()
		player_val = self.state.player_hand.calc_val()

		if dealer_val > 21:
			self.state.result = 'Dealer busts! You win! ' + self.restart_phrase
			self.state.chip_pool += self.state.bet
		elif dealer_val < player_val:
			self.state.result = 'You beat the dealer, you win! ' + self.restart_phrase
			self.state.chip_pool += self.state.bet
		elif dealer_val == player_val:
			self.state.result = 'Tied up, push!' + self.restart_phrase
		else:
			self.state.result = 'Dealer Wins! ' + self.restart_phrase
			self.state.chip_pool -= self.state.bet

		self.state.playing = False
		self.state.show_all_cards = True
		return True

	def get_game_state(self):
		"""Return current game state as a dictionary"""
		return {
			'playing': self.state.playing,
			'chip_pool': self.state.chip_pool,
			'bet': self.state.bet,
			'player_hand': self.state.player_hand.get_visible_cards() if self.state.player_hand else [],
			'dealer_hand': self.state.dealer_hand.get_visible_cards(hidden=True, show_all=self.state.show_all_cards) if self.state.dealer_hand else [],
			'player_score': self.state.player_hand.calc_val() if self.state.player_hand else 0,
			'dealer_score': self.state.dealer_hand.calc_val() if self.state.dealer_hand else 0,
			'result': self.state.result
		}

# Create a singleton instance
game = BlackjackGame()
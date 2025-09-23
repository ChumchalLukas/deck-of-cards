from collections import deque
import random
import copy


# Constant - card values, suits, worthness


CARD_SUITS = {
    "SPADE":("\u2660",chr(0x2660)),
    "HEART":("\u2665",chr(0x2665)),
    "DIAMOND":("\u2666",chr(0x2666)),
    "CLUB":("\u2663",chr(0x2663))
}

CARD_WORTH = {
    "A" : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "10": 10,
    "J" : 10,
    "Q" : 10,
    "K" : 10,

}

class Card:
    def __init__(self, suit : str, value : str) -> None:
        self._validate_suit(suit)
        self._validate_value(value)

        self.__suit = suit
        self.__value = value
        self.__worth = CARD_WORTH[value]
        self.visualize = None

    def _validate_suit(self, suit : str) -> None:
        """Validation of suit type and values."""

        valid_suits = []
        for utf_char, char_literal in CARD_SUITS.values():
            valid_suits.extend([utf_char, char_literal])
    
        if suit not in valid_suits:
            raise ValueError(f"Card object does not have valid suit: {suit}")


    def _validate_value(self, value: str) -> None:
        """Validation correct card type and values"""

        if not isinstance(value, str):
            raise TypeError(f"Card value has invalid type: {type(value)}")
        if value not in CARD_WORTH:
            raise ValueError(f"Card object does not have valid value: {value}")

    @property
    def value(self):
        """Return cards value symbol."""
        return self.__value

    @property
    def suit(self):
        """Return cards suit symbol."""
        return self.__suit

    @property
    def worth(self):
        """Return cards curent true worthness."""
        return self.__worth

    @worth.setter
    def worth(self, new_worth: int) -> None:
        """Set new card worth value.

        Args:
            new_worth: Integer between 1 and 11 representing card worth.

        Raises:
            TypeError: If new_worth is not an integer.
            ValueError: If new_worth is not between 1 and 11.
        """
        if not isinstance(new_worth, int):
            raise TypeError("New worth must be an integer.")
        if not (1 <= new_worth <= 11):
            raise ValueError("Worth must be between 1 and 11.")
        self.__worth = new_worth
        
    # Card creation:

    def to_render(self) -> list[str]:
        """Create ASCII art representation of the card.
    
        Returns:
            List of strings representing card lines for display.
        """

        card_symbol = self.suit.rjust(len(self.suit) + 3, " ").ljust(len(self.suit) + 4, " ")
        card_value = self.value.ljust(len(self.value) + 2, " ").rjust(len(self.value) + 3, " ") if self.value == "10" else self.value.ljust(len(self.value) + 3, " ").rjust(len(self.value) + 4, " ")


        top = "|=====|"
        level1 = f"|{card_value}|"
        level2 = "|     |"
        level3 = f"|{card_symbol}|"
        bottom = "|=====|"

        self.visualize = [top, level1, level2, level3, bottom]

        return self.visualize

    def __repr__(self):
        return f"Card(suit = {self.suit}, value = {self.value}, worth = {self.worth})"
    
    def __str__(self):
        
        card_symbol = self.suit.rjust(len(self.suit) + 3, " ").ljust(len(self.suit) + 4, " ")
        card_value = self.value.ljust(len(self.value) + 2, " ").rjust(len(self.value) + 3, " ") if self.value == "10" else self.value.ljust(len(self.value) + 3, " ").rjust(len(self.value) + 4, " ")

        
        card = f"""

            |=====|
            |{card_value}|
            |     |
            |{card_symbol}|
            |=====|

            suit:  {self.suit}
            value: {self.value}
            worth: {self.worth}


        """

        return card
    

class DeckOfCards:


    def __init__(self) -> None:

        self._cards_count = 0
        self._destroyed_cards = 0
        self._dealt_cards = 0 

    @property
    def deck_cards(self) -> int:
        """Get how much cards in created deck."""
        return self._cards_count
        
    @deck_cards.setter
    def deck_cards(self,value : int) -> None:
        """Set new value as card counts in deck."""
        self._cards_count = value
        
    @property
    def discarded_cards(self) -> int:
        """Counts of how much cards are thrown away."""
        return self._destroyed_cards
        
    @discarded_cards.setter
    def discarded_cards(self, value : int) -> None:
        """Set new value for discarded counts."""
        self._destroyed_cards = value


    @property
    def dealt_cards(self) -> int:
        """Counts how many cards have been dealt to players."""
        return self._dealt_cards
        
    @dealt_cards.setter
    def dealt_cards(self, value : int) -> None:
        """Set new count for dealt cards."""
        self._dealt_cards = value
        
        

    def create_deck(self, count : int = 1) -> deque[Card]:
        """Create a shuffled deck of playing cards.
    
        Args:
            count: Number of standard 52-card decks to combine.
        
        Returns:
            Shuffled deque containing Card objects.
        """
            
        # set decks card counts, main data structure:
        self.deck_cards = count * 52
        basic_deck = deque()
        multiple_decks = deque()

        # adding cards to basic deck:
        for suit in CARD_SUITS.keys():
            for value in CARD_WORTH.keys():

                basic_deck.append(Card(suit, value))

        # creating multiple/one deque decks:

        if count > 1:

            decks_done = 0

            while decks_done != count:

                basic_deck_copy = copy.deepcopy(basic_deck)

                multiple_decks.extend(basic_deck_copy)

                decks_done += 1

                lst_multiple_decks = list(multiple_decks)
                random.shuffle(lst_multiple_decks)

            return deque(lst_multiple_decks)
            
        lst_basic_deck = list(basic_deck)
        random.shuffle(lst_basic_deck)

        return deque(lst_basic_deck)
                    



    def deal_card(self, deck : deque[Card], side : str = "top") -> Card:
        """Deal a card from the deck.
    
        Args:
            deck: The deck to deal from.
            side: Which end to deal from ('top' or 'bottom').
        
        Returns:
            The dealt Card object.
    """

        if side == "bottom":

            self.dealt_cards += 1

            return deck.pop()
            
        self.dealt_cards += 1
            
        return deck.popleft() 


    def discard_card(self, deck : deque[Card], side : str = "top") -> None:
        """Discard a card from deck
    
        Args:
            deck: The deck to deal from.
            side: Which end to deal from ('top' or 'bottom').

        """

        if side == "bottom":

            self.discarded_cards += 1

            deck.pop()

        else:

            self.discarded_cards += 1

            deck.popleft()
        

    @staticmethod
    def display_cards(*cards: Card) -> None:
        """Visualization cards line by line in ASCII art fascion. """

        for lines in zip(*cards):
            print(lines)

    def __str__(self):
        return f"Regular deck playing cards: packets = {self.deck_cards/4}"
        
    def __repr__(self):
        return f"DeckOfCards(card_count = {self.deck_cards}, card_dealt = {self.dealt_cards}, destroy_cards = {self.discarded_cards})"
        




import random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        if rank == "Ace":
            self.value = 11
        elif rank in ["Jack", "Queen", "King"]:
            self.value = 10
        else:
            self.value = int(rank)

    def __repr__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self, num_decks=1):
        self.cards = []
        for _ in range(num_decks):
            for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
                for rank in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]:
                    self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Blackjack:
    def __init__(self, num_decks=1):
        self.deck = Deck(num_decks)
        while True:
            try:
                self.player_funds = float(input("How much would you like to deposit?: "))
                if self.player_funds > 0:
                    break
            except ValueError:
                print("Please enter a valid number.")

    def place_bet(self):
        while True:
            try:
                bet = float(input("Enter your bet: "))
                if self.player_funds >= bet > 0:
                    return bet
                else:
                    print("Please enter a valid bet.")
            except ValueError:
                print("Please enter a valid number.")

    def play_game(self):
        while True:
            if len(self.deck.cards) < 10:
                self.deck = Deck()
                self.deck.shuffle()

            bet = self.place_bet()

            self.deck.shuffle()

            player_hand = [self.deck.deal_card(), self.deck.deal_card()]
            dealer_hand = [self.deck.deal_card(), self.deck.deal_card()]

            print("Player's hand:", player_hand)
            print("Dealer's hand:", [dealer_hand[0], "<hidden>"])

            while sum(card.value for card in player_hand) < 21:
                choice = input("Do you want to hit, stand, or double down? ")
                if choice.lower() == "hit":
                    new_card = self.deck.deal_card()
                    player_hand.append(new_card)
                    print("Player's hand:", player_hand)
                    if sum(card.value for card in player_hand) > 21:
                        print("Player busts! Dealer wins.")
                        self.player_funds -= bet

                elif choice.lower() == "stand":
                    break

                elif choice.lower() == "double down":
                    if bet*2 > self.player_funds:
                        print("You don't have enough funds to double down.")
                        choice = input("Do you want to hit or stand? ")
                        if choice.lower() == "hit":
                            new_card = self.deck.deal_card()
                            player_hand.append(new_card)
                            print("Player's hand:", player_hand)
                            if sum(card.value for card in player_hand) > 21:
                                print("Player busts! Dealer wins.")
                                self.player_funds -= bet

                        elif choice.lower() == "stand":
                            break

                    elif len(player_hand) == 2:
                        bet *= 2
                        new_card = self.deck.deal_card()
                        player_hand.append(new_card)
                        print("Player's hand:", player_hand)
                        if sum(card.value for card in player_hand) > 21:
                            print("Player busts! Dealer wins.")
                            self.player_funds -= bet
                            break
                        else:
                            break
                    else:
                        print("You can only double down with your initial hand.")

            while sum(card.value for card in dealer_hand) < 17:
                dealer_hand.append(self.deck.deal_card())

            player_total = sum(card.value for card in player_hand)
            dealer_total = sum(card.value for card in dealer_hand)
            print("Player's hand:", player_hand)
            print("Dealer's hand:", dealer_hand)
            if player_total > 21:
                print("Player busts! Dealer wins.")
                self.player_funds -= bet
            elif player_total == 21 and dealer_total != 21:
                print("Player Blackjack!")
                self.player_funds += bet * 1.5
            elif dealer_total == 21 and player_total < 21:
                print("Dealer Blackjack!")
                self.player_funds -= bet
            elif player_total != 21 and player_total > dealer_total:
                print("Player wins!")
                self.player_funds += bet
            elif dealer_total > 21:
                print("Dealer busts! Player wins.")
                self.player_funds += bet
            elif dealer_total > player_total:
                print("Dealer wins!")
                self.player_funds -= bet
            else:
                print("It's a tie!")

            if self.player_funds <= 0:
                print("You ran out of funds! You lose.")
                quit()
            print("Remaining funds:", self.player_funds)


while True:
    try:
        num_decks = int(input("How many decks do you want to use? "))
        if num_decks > 0:
            break
        else:
            print("Please enter a positive number.")
    except ValueError:
        print("Please enter a valid number.")


game = Blackjack(num_decks)
game.play_game()

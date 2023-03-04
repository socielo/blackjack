import random as r

# Decided to make this for fun, kind of buggy.
# Aces are always 11.
# Dealer stands on 17 always
# Double down can only draw one extra card
# Min bet $1.00
# One Deck
# Some blackjack rules may be wrong, haven't played in a year

# Eventually will try to add a gui and implement it into OOP


def blackjack():

    playable_deck = ['2H-2', '3H-3', '4H-4', '5H-5', '6H-6', '7H-7', '8H-8',
                     '9H-9', '10H-10', 'AH-11', 'JH-10', 'QH-10', 'KH-10',
                     '2D-2', '3D-3', '4D-4', '5D-5', '6D-6', '7D-7', '8D-8',
                     '9D-9', '10D-10', 'AD-11', 'JD-10', 'QD-10', 'KD-10',
                     '2C-2', '3C-3', '4C-4', '5C-5', '6C-6', '7C-7', '8C-8',
                     '9C-9', '10C-10', 'AC-11', 'JC-10', 'QC-10', 'KC-10',
                     '2S-2', '3S-3', '4S-4', '5S-5', '6S-6', '7S-7', '8S-8',
                     '9S-9', '10S-10', 'AS-11', 'JS-10', 'QS-10', 'KS-10'
                    ]
    play_again = "Y"
    while play_again == "Y":
        while play_again == "Y":

            money = input("How much would you like to deposit? ")
            try:
                money = float(money)

                total_money =+ money
                break
            except ValueError:
                print("Please enter a valid number.")

        try:
            while len(playable_deck) > 4:
                while True:
                    if money <= 0:
                        print("You ran out of money!")
                        play_again = input("Would you like to play again? [Y, N]: ")
                        if play_again == "Y":
                            playable_deck = ['2H-2', '3H-3', '4H-4', '5H-5', '6H-6', '7H-7', '8H-8',
                                             '9H-9', '10H-10', 'AH-11', 'JH-10', 'QH-10', 'KH-10',
                                             '2D-2', '3D-3', '4D-4', '5D-5', '6D-6', '7D-7', '8D-8',
                                             '9D-9', '10D-10', 'AD-11', 'JD-10', 'QD-10', 'KD-10',
                                             '2C-2', '3C-3', '4C-4', '5C-5', '6C-6', '7C-7', '8C-8',
                                             '9C-9', '10C-10', 'AC-11', 'JC-10', 'QC-10', 'KC-10',
                                             '2S-2', '3S-3', '4S-4', '5S-5', '6S-6', '7S-7', '8S-8',
                                             '9S-9', '10S-10', 'AS-11', 'JS-10', 'QS-10', 'KS-10'
                                             ]
                            while money != float:
                                money = input("How much would you like to deposit? ")
                                try:
                                    money = float(money)
                                    break
                                except ValueError:
                                    print("Please enter a valid number.")
                        elif play_again == "N":
                            quit()
                        while play_again not in ["Y", "N"]:
                            play_again = input("Would you like to play again? [Y, N]: ")
                            if play_again == "Y":
                                playable_deck = ['2H-2', '3H-3', '4H-4', '5H-5', '6H-6', '7H-7', '8H-8',
                                                 '9H-9', '10H-10', 'AH-11', 'JH-10', 'QH-10', 'KH-10',
                                                 '2D-2', '3D-3', '4D-4', '5D-5', '6D-6', '7D-7', '8D-8',
                                                 '9D-9', '10D-10', 'AD-11', 'JD-10', 'QD-10', 'KD-10',
                                                 '2C-2', '3C-3', '4C-4', '5C-5', '6C-6', '7C-7', '8C-8',
                                                 '9C-9', '10C-10', 'AC-11', 'JC-10', 'QC-10', 'KC-10',
                                                 '2S-2', '3S-3', '4S-4', '5S-5', '6S-6', '7S-7', '8S-8',
                                                 '9S-9', '10S-10', 'AS-11', 'JS-10', 'QS-10', 'KS-10'
                                                 ]
                                money = input("How much would you like to deposit? ")
                            elif play_again == "N":
                                quit()
                    print(f"Your balance is ${money:.2f}")

                    while True:
                        try:
                            bet = input("How much would you like to bet? ")
                            bet = float(bet)
                            break
                        except ValueError:
                            print("Please enter a valid number")
                    while bet > money:
                        print("You cannot bet more money than you have.")
                        bet = input("What would you like to bet? ")
                        bet = float(bet)
                    while bet < 1:
                        print("Minimum bet is $1.00")
                        bet = float(input("What would you like to bet? "))

                    dealer_choice = r.choice(playable_deck)
                    player_choice = r.choice(playable_deck)

                    playable_deck.remove(dealer_choice)
                    playable_deck.remove(player_choice)

                    dealer_card = dealer_choice.split("-")
                    player_card = player_choice.split("-")

                    dealer = int(dealer_card[1])
                    player = int(player_card[1])

                    print(f"Dealer's Card: {dealer_card[0]}, Value: {dealer_card[1]}")
                    print(f"Player's Card: {player_card[0]}, Value: {player_card[1]}")
                    double_down = "N"
                    if bet*2 <= money:
                        double_down = str(input("Would you like to double down? [Y, N] "))
                        if double_down == "Y":
                            bet *= 2
                        while double_down != "Y" and double_down != "N":
                            double_down = str(input("Would you like to double down? [Y, N] "))

                        if double_down == "Y":
                            player_choice2 = r.choice(playable_deck)
                            playable_deck.remove(player_choice2)
                            player_card2 = player_choice2.split("-")
                            player2 = int(player_card2[1])
                            player += player2
                            print(f"Player card: {player_card2}")
                            print(f"Player total: {player}")

                    while player < 21:
                        if double_down == "Y":
                            break
                        hit_or_stand = str(input("Would you like to hit? [Y, N]:  "))
                        if hit_or_stand == "Y":
                            player_choice2 = r.choice(playable_deck)
                            playable_deck.remove(player_choice2)
                            player_card2 = player_choice2.split("-")
                            player2 = int(player_card2[1])
                            player += player2
                            print(f"Player Card: {player_card2}")
                            print(f"Player total: {player}")
                        if player > 21:
                            print("Player busted!")
                            money -= bet
                            break
                        elif player == 21:
                            print("Player: Blackjack!")

                        if hit_or_stand == "N":
                            break

                    while dealer < 17:
                        if player > 21:
                            break
                        dealer_choice2 = r.choice(playable_deck)
                        playable_deck.remove(dealer_choice2)
                        dealer_card2 = dealer_choice2.split("-")
                        dealer2 = int(dealer_card2[1])
                        dealer += dealer2
                        print(f"Dealer's Card: {dealer_card2}")
                        print(f"Dealer total: {dealer}")

                        if dealer > 21:
                            print("Dealer busted")
                            money += bet
                            break
                        elif dealer == 21:
                            print("Dealer: Blackjack!")
                            if player < 21:
                                money -= bet

                        if dealer == 21 and player == 21:
                            print("Push")
                            break
                    if dealer != 21 and player == 21:
                        money += bet * 1.5

                    elif player < 21 and player < dealer < 21:
                        money -= bet

                    elif 21 > player > dealer and dealer < 21:
                        money += bet
        except IndexError:
            print(f"Out of cards, Game Over\n"
                  f"Your balance is ${money:.2f}")
            play_again = input("Would you like to play again? [Y, N]: ")
            if play_again == "Y":
                playable_deck = ['2H-2', '3H-3', '4H-4', '5H-5', '6H-6', '7H-7', '8H-8',
                                 '9H-9', '10H-10', 'AH-11', 'JH-10', 'QH-10', 'KH-10',
                                 '2D-2', '3D-3', '4D-4', '5D-5', '6D-6', '7D-7', '8D-8',
                                 '9D-9', '10D-10', 'AD-11', 'JD-10', 'QD-10', 'KD-10',
                                 '2C-2', '3C-3', '4C-4', '5C-5', '6C-6', '7C-7', '8C-8',
                                 '9C-9', '10C-10', 'AC-11', 'JC-10', 'QC-10', 'KC-10',
                                 '2S-2', '3S-3', '4S-4', '5S-5', '6S-6', '7S-7', '8S-8',
                                 '9S-9', '10S-10', 'AS-11', 'JS-10', 'QS-10', 'KS-10'
                                 ]
            elif play_again == "N":
                print("Thanks for playing!")
                quit()
            while play_again not in ["Y", "N"]:
                play_again = input("Would you like to play again? [Y, N]: ")
                if play_again == "Y":
                    playable_deck = ['2H-2', '3H-3', '4H-4', '5H-5', '6H-6', '7H-7', '8H-8',
                                     '9H-9', '10H-10', 'AH-11', 'JH-10', 'QH-10', 'KH-10',
                                     '2D-2', '3D-3', '4D-4', '5D-5', '6D-6', '7D-7', '8D-8',
                                     '9D-9', '10D-10', 'AD-11', 'JD-10', 'QD-10', 'KD-10',
                                     '2C-2', '3C-3', '4C-4', '5C-5', '6C-6', '7C-7', '8C-8',
                                     '9C-9', '10C-10', 'AC-11', 'JC-10', 'QC-10', 'KC-10',
                                     '2S-2', '3S-3', '4S-4', '5S-5', '6S-6', '7S-7', '8S-8',
                                     '9S-9', '10S-10', 'AS-11', 'JS-10', 'QS-10', 'KS-10'
                                    ]
                elif play_again == "N":
                    print("Thanks for playing!")
                    quit()


blackjack()


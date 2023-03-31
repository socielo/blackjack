from tkinter import *
from tkinter import messagebox
import random as r
from PIL import ImageTk, Image
from tkinter import simpledialog
global balance, bet

root = Tk()
root.title("Blackjack")
root.iconbitmap("cards/icon.png")
root.geometry("1200x800")
root.configure(bg="green")

balance = 0
deposited = False
bet_placed = False
bet_amount = 0


def deposit():
    global balance, deposited
    if not deposited:
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:", parent=root)
        if amount is not None and amount >= 10:
            balance += amount
            balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
            deposit_button.config(state=DISABLED, highlightbackground='green', highlightcolor='green')
            bet_button.config(state=NORMAL, highlightbackground='green', highlightcolor='green')
            deposited = True
        else:
            messagebox.showinfo("Invalid Deposit", "The minimum deposit is $10")


def bet():
    global balance, bet_amount, bet_placed, player_score, dealer_score, dealer_spot, player_spot
    amount = simpledialog.askfloat("Bet", "Enter amount to bet:", parent=root)

    if 10 <= amount <= balance:
        shuffle()

    if 10 <= amount <= balance and dealer_score not in [17, 18, 19, 20, 21]:
        balance -= amount
        bet_amount = amount
        balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
        bet_placed = True
        bet_button.config(state=DISABLED)
        card_button.config(state=NORMAL)
        stand_button.config(state=NORMAL)
        if player_spot > 2 or dealer_spot > 2 or dealer_score in [17, 18, 19, 20, 21]:
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)

    else:
        messagebox.showinfo("Invalid Bet", "The bet must be greater or equal to $10 and less than the balance")
        return

    if blackjack_status["player"] == "yes" or blackjack_status["dealer"] == "yes":
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)



def stand():
    global player_total, dealer_total, player_score, balance, bet_amount
    player_total = 0
    dealer_total = 0

    for score in dealer_score:
        dealer_total += score

    for score in player_score:
        player_total += score

    card_button.config(state=DISABLED)
    stand_button.config(state=DISABLED)
    bet_button.config(state=NORMAL)

    if dealer_total >= 17:
        if dealer_total > 21:
            messagebox.showinfo("Player wins!", "Bust: Dealer busted!")
            balance += bet_amount*2
            balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
            return
        elif dealer_total == player_total:
            messagebox.showinfo("Push!", "Push: It's a tie!")
            balance += bet_amount
            balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
            return
        elif dealer_total > player_total:
            messagebox.showinfo("Dealer Wins!", "Dealer Wins: Dealer wins!")
            return
        else:
            messagebox.showinfo("Player Wins!", "Player Wins: Player wins!")
            balance += bet_amount*2
            balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
            return
    else:
        dealer_hit()
        stand()

def blackjack_shuffle(player):
    global player_total, dealer_total, player_score, balance, bet_amount, player_spot, dealer_spot
    if player_spot == 2 and player_score == 21:
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)

    if dealer_spot == 2 and dealer_score == 21:
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)

    if player_spot == 2 and player_score == 21 and dealer_spot == 2 and player_score == 21:
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)
    player_total = 0
    dealer_total = 0
    if player == "dealer":
        if len(dealer_score) == 2:
            if dealer_score[0] + dealer_score[1] == 21:
                blackjack_status["dealer"] = "yes"
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)

    if player == "player":
        if len(player_score) == 2:
            if player_score[0] + player_score[1] == 21:
                blackjack_status["player"] = "yes"
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)

        else:
            for score in player_score:
                player_total += score

            if player_total == 21:
                blackjack_status["player"] = "yes"
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)

            elif player_total > 21:
                for card_num, card in enumerate(player_score):
                    if card == 11:
                        player_score[card_num] = 1
                        player_total = 0
                        for score in player_score:
                            player_total += score
                        if player_total > 21:
                            blackjack_status["player"] = "bust"

                else:
                    if player_total == 21:
                        blackjack_status["player"] = "yes"
                        card_button.config(state=DISABLED)
                        stand_button.config(state=DISABLED)
                        bet_button.config(state=NORMAL)
                    if player_total > 21:
                        blackjack_status["player"] = "bust"

            for score in dealer_score:
                dealer_total += score

            if player_total == 21:
                blackjack_status["player"] = "yes"
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)
            if dealer_total > 21:
                for card_num, card in enumerate(dealer_score):
                    if card == 11:
                        dealer_score[card_num] = 1
                        dealer_total = 0
                        for score in dealer_score:
                            dealer_total += score
                        if dealer_total > 21:
                            blackjack_status["dealer"] = "bust"

                else:
                    if dealer_total == 21:
                        blackjack_status["dealer"] = "yes"
                    if dealer_total > 21:
                        blackjack_status["dealer"] = "bust"

    if len(dealer_score) == 2 and len(player_score) == 2:
        if blackjack_status["dealer"] == "yes" and blackjack_status["player"] == "yes":
            messagebox.showinfo("Push!", "Push: It's a Tie!")
            balance += bet_amount
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            bet_button.config(state=NORMAL)
            balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
            return

        elif blackjack_status["dealer"] == "yes":
            messagebox.showinfo("Blackjack!", "Blackjack: Dealer Wins!")
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            bet_button.config(state=NORMAL)

            return

        elif blackjack_status["player"] == "yes":
            balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
            messagebox.showinfo("Blackjack!", "Blackjack: Player Wins!")
            balance += bet_amount * 2.5
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            bet_button.config(state=NORMAL)
            balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
            return

    else:
        if blackjack_status["dealer"] == "yes" and blackjack_status["player"] == "yes":
            messagebox.showinfo("Push!", "Push: It's a Tie!")
            balance += bet_amount
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            bet_button.config(state=NORMAL)
            balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
            return

        elif blackjack_status["dealer"] == "yes":
            if len(dealer_score) > 2:
                messagebox.showinfo("21!", "21: Dealer Wins!")
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)
                balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
                return

        elif blackjack_status["player"] == "yes":
            if len(player_score) > 2:
                messagebox.showinfo("21!", "21: Player Wins!")
                balance += bet_amount*2
                balance_label.config(text=f"Balance: {balance:.2f}", bg='green')
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)
                return

    if blackjack_status["player"] == "bust":
        messagebox.showinfo("Bust!", "Player Busts!")
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)
        return


def resize_cards(card):
    global our_card_image
    our_card_image = Image.open(card)
    our_card_resize = our_card_image.resize((150, 218))
    our_card_image = ImageTk.PhotoImage(our_card_resize)
    return our_card_image

def shuffle():
    global blackjack_status, player_total, dealer_total, card_button, stand_button
    global dealer, player, dealer_spot, player_spot, dealer_score, player_score, deck
    bet_button.config(state=DISABLED)
    card_button.config(state=NORMAL)
    stand_button.config(state=NORMAL)

    player_total = 0
    dealer_total = 0

    blackjack_status = {"dealer": "no", "player": "no"}

    dealer_label_1.config(image="")
    dealer_label_2.config(image="")
    dealer_label_3.config(image="")
    dealer_label_4.config(image="")
    dealer_label_5.config(image="")

    player_label_1.config(image="")
    player_label_2.config(image="")
    player_label_3.config(image="")
    player_label_4.config(image="")
    player_label_5.config(image="")

    suits = ["hearts", "diamonds", "clubs", "spades"]
    values = range(2, 15)

    deck = []
    for suit in suits:
        for value in values:
            deck.append(f"{value}_of_{suit}")

    dealer = []
    player = []
    dealer_score = []
    player_score = []
    dealer_spot = 0
    player_spot = 0

    for _ in range(2):
        player_hit()
        dealer_hit()
    root.title(f"Blackjack")

    if balance == 0 and dealer_spot > 2 or player_spot > 2:
        messagebox.showinfo("Insufficient Funds", "You don't have enough funds to play!")
        quit()


def dealer_hit():
    global dealer_spot, player_total, dealer_total, player_score
    global dealer_image1, dealer_image2, dealer_image3, dealer_image4, dealer_image5
    if blackjack_status["player"] == "yes" or blackjack_status["dealer"] == "yes":
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)
    if dealer_spot <= 5:
        try:
            dealer_card = r.choice(deck)
            deck.remove(dealer_card)
            dealer.append(dealer_card)
            dcard = int(dealer_card.split("_", 1)[0])
            if dcard == 14:
                dealer_score.append(11)
            elif dcard in [11, 12, 13]:
                dealer_score.append(10)
            else:
                dealer_score.append(dcard)


            if dealer_spot == 0:
                dealer_image1 = resize_cards(f"cards/{dealer_card}.png")
                dealer_label_1.config(image=dealer_image1)
                dealer_spot += 1

            elif dealer_spot == 1:
                dealer_image2 = resize_cards(f"cards/{dealer_card}.png")
                dealer_label_2.config(image=dealer_image2)
                dealer_spot += 1

            elif dealer_spot == 2:
                dealer_image3 = resize_cards(f"cards/{dealer_card}.png")
                dealer_label_3.config(image=dealer_image3)
                dealer_spot += 1

            elif dealer_spot == 3:
                dealer_image4 = resize_cards(f"cards/{dealer_card}.png")
                dealer_label_4.config(image=dealer_image4)
                dealer_spot += 1

            elif dealer_spot == 4:
                dealer_image5 = resize_cards(f"cards/{dealer_card}.png")
                dealer_label_5.config(image=dealer_image5)
                dealer_spot += 1

                player_total = 0
                dealer_total = 0

                for score in player_score:
                    player_total += score

                for score in dealer_score:
                    dealer_total += score

                if dealer_total <= 21:
                    card_button.config(state=DISABLED)
                    stand_button.config(state=DISABLED)
                    bet_button.config(state=NORMAL)
                    messagebox.showinfo("Dealer wins!", "Dealer wins: Dealer Wins!")

            root.title(f"Blackjack")

        except:
            root.title("Blackjack | Cards left: 0")

        blackjack_shuffle("dealer")


    if player_spot == 2 and player_score == 21:
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)

    if dealer_spot == 2 and dealer_score == 21:
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)

    if player_spot == 2 and player_score == 21 and dealer_spot == 2 and player_score == 21:
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)


def player_hit():
    global player_spot, dealer_total, player_total, player_score, balance, bet_amount
    global player_image1, player_image2, player_image3, player_image4, player_image5
    if blackjack_status["player"] == "yes" or blackjack_status["dealer"] == "yes":
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)
    if player_spot <= 5:
        try:
            player_card = r.choice(deck)
            deck.remove(player_card)
            player.append(player_card)
            pcard = int(player_card.split("_", 1)[0])
            if pcard == 14:
                player_score.append(11)
            elif pcard in [11, 12, 13]:
                player_score.append(10)
            else:
                player_score.append(pcard)

            if player_spot == 0:
                player_image1 = resize_cards(f"cards/{player_card}.png")
                player_label_1.config(image=player_image1)
                player_spot += 1

            elif player_spot == 1:
                player_image2 = resize_cards(f"cards/{player_card}.png")
                player_label_2.config(image=player_image2)
                player_spot += 1

            elif player_spot == 2:
                player_image3 = resize_cards(f"cards/{player_card}.png")
                player_label_3.config(image=player_image3)
                player_spot += 1

            elif player_spot == 3:
                player_image4 = resize_cards(f"cards/{player_card}.png")
                player_label_4.config(image=player_image4)
                player_spot += 1

            elif player_spot == 4:
                player_image5 = resize_cards(f"cards/{player_card}.png")
                player_label_5.config(image=player_image5)
                player_spot += 1
                player_total = 0
                dealer_total = 0

                for score in player_score:
                    player_total += score

                for score in dealer_score:
                    dealer_total += score

                if player_total <= 21:
                    card_button.config(state=DISABLED)
                    stand_button.config(state=DISABLED)
                    bet_button.config(state=NORMAL)
                    balance += bet_amount*2
                    messagebox.showinfo("Player wins!", "Player wins: Player Wins!")

            root.title(f"Blackjack")

        except:
            root.title("Blackjack | Cards left: 0")

        blackjack_shuffle("player")


def deal_cards():
    try:
        card = r.choice(deck)
        deck.remove(card)
        dealer.append(card)
        global dealer_image
        dealer_image = resize_cards(f"cards/{card}.png")

        card = r.choice(deck)
        deck.remove(card)
        player.append(card)
        global player_image
        player_image = resize_cards(f"cards/{card}.png")

        root.title(f"Blackjack")

    except:
        root.title("Blackjack | Cards left: 0")




my_frame = Frame(root, bg='green')
my_frame.pack(pady=25)

dealer_frame = LabelFrame(my_frame, text="| Dealer Hand |", bd=0, bg='green', labelanchor='n')
dealer_frame.pack(padx=20, ipadx=20)

player_frame = LabelFrame(my_frame, text="| Player Hand |", bd=0, bg='green', labelanchor='n')
player_frame.pack(ipadx=20, pady=10)

dealer_label_1 = Label(dealer_frame, text='', bg='green')
dealer_label_1.grid(row=0, column=0, pady=20, padx=20)

dealer_label_2 = Label(dealer_frame, text='', bg='green')
dealer_label_2.grid(row=0, column=1, pady=20, padx=20)

dealer_label_3 = Label(dealer_frame, text='', bg='green')
dealer_label_3.grid(row=0, column=2, pady=20, padx=20)

dealer_label_4 = Label(dealer_frame, text='', bg='green')
dealer_label_4.grid(row=0, column=3, pady=20, padx=20)

dealer_label_5 = Label(dealer_frame, text='', bg='green')
dealer_label_5.grid(row=0, column=4, pady=20, padx=20)

player_label_1 = Label(player_frame, text='', bg='green')
player_label_1.grid(row=1, column=0, pady=20, padx=20)

player_label_2 = Label(player_frame, text='', bg='green')
player_label_2.grid(row=1, column=1, pady=20, padx=20)

player_label_3 = Label(player_frame, text='', bg='green')
player_label_3.grid(row=1, column=2, pady=20, padx=20)

player_label_4 = Label(player_frame, text='', bg='green')
player_label_4.grid(row=1, column=3, pady=20, padx=20)

player_label_5 = Label(player_frame, text='', bg='green')
player_label_5.grid(row=1, column=4, pady=20, padx=20)

money_frame = Frame(root, bg='green')
money_frame.pack(side=TOP, pady=10,)

balance_label = Label(money_frame, text=f"Balance: {balance:.2f}", bg='green')
balance_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='n')

deposit_button = Button(money_frame, text="Deposit", highlightbackground='green', highlightcolor='green',
                        command=deposit)
deposit_button.grid(row=1, column=0, pady=10, sticky='e')

bet_button = Button(money_frame, text="Bet", highlightbackground='green', highlightcolor='green',
                    command=bet, state=DISABLED)
bet_button.grid(row=1, column=1, pady=10, sticky='w')

button_frame = Frame(root, bg='green')
button_frame.pack(side=BOTTOM, pady=15)

card_button = Button(button_frame, text="Hit", bg='green', font=("Arial", 15), command=player_hit,
                     padx=20, pady=10, highlightbackground='green')
card_button.pack(side=LEFT)

stand_button = Button(button_frame, text="Stand", bg='green', font=("Arial", 15), command=stand,
                      padx=20, pady=10, highlightbackground='green')
stand_button.pack(side=LEFT)

card_button.config(state=DISABLED)
stand_button.config(state=DISABLED)

root.mainloop()


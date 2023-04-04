from tkinter import (
    Tk,
    DISABLED,
    NORMAL,
    Frame,
    LabelFrame,
    Label,
    TOP,
    Button,
    BOTTOM,
    LEFT,
    messagebox,
    simpledialog,
)
from PIL import ImageTk, Image
import random as r
import pygame.mixer

root = Tk()
root.title("Blackjack")
root.iconbitmap("cards/icon.png")
root.geometry("1200x800")
root.configure(bg="green")

balance = 0
bet_amount = 0
deposited = False
bet_placed = False
player_score = []


def play_sound(sound):
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()


def deposit():
    global balance, deposited
    if not deposited:
        amount = simpledialog.askfloat(
            "Deposit", "Enter amount to deposit:", parent=root
        )
        if amount is not None and amount >= 10:
            balance += amount
            balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
            deposit_button.config(
                state=DISABLED, highlightbackground="green", highlightcolor="green"
            )
            bet_button.config(
                state=NORMAL, highlightbackground="green", highlightcolor="green"
            )
            deposited = True
        else:
            messagebox.showinfo("Invalid Deposit", "The minimum deposit is $10.")


def bet():
    global balance, bet_amount, bet_placed
    amount = simpledialog.askfloat("Bet", "Enter amount to bet:", parent=root)
    if 5 <= amount <= balance:
        shuffle()
        card_button.pack(side=LEFT)
        stand_button.pack(side=LEFT)

    if 5 <= amount <= balance:
        balance -= amount
        bet_amount = amount
        balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
        bet_placed = True
        bet_button.config(state=DISABLED)
        card_button.config(state=NORMAL)
        stand_button.config(state=NORMAL)
    else:
        if balance < 5:
            messagebox.showinfo("Insufficient Funds", "You ran out of funds!")

            quit()

        else:
            messagebox.showinfo(
                "Invalid Bet",
                "The bet must be greater or equal to $5 and less than the balance.",
            )
        return

    if blackjack_status["player"] == "yes" or blackjack_status["dealer"] == "yes":
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        bet_button.config(state=NORMAL)


def stand():
    global balance, bet_amount

    player_total = 0
    dealer_total = 0

    for score in dealer_score:
        dealer_total += score

    for score in player_score:
        player_total += score

    if dealer_total >= 17:
        if dealer_total > 21:
            for card_num, card in enumerate(dealer_score):
                if card == 11:
                    dealer_score[card_num] = 1
                    dealer_total = 0
                    for score in dealer_score:
                        dealer_total += score
        if player_total > 21:
            for card_num, card in enumerate(player_score):
                if card == 11:
                    player_score[card_num] = 1
                    player_total = 0
                    for score in player_score:
                        player_total += score
                    if player_total > 21:
                        blackjack_status["player"] = "bust"

        if dealer_total > 21:
            dealer_image1 = dealer_image_1_show
            dealer_label_1.config(image=dealer_image1)
            play_sound("sounds/win.mp3")
            messagebox.showinfo("Player wins!", "Dealer busts: Player wins!")
            balance += bet_amount * 2
            balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
            bet_button.config(state=NORMAL)
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            return
        elif dealer_total == player_total and dealer_spot != 5:
            messagebox.showinfo("Push!", "Push: It's a tie!")
            balance += bet_amount
            dealer_image1 = dealer_image_1_show
            dealer_label_1.config(image=dealer_image1)
            balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
            bet_button.config(state=NORMAL)
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            return
        elif dealer_total > player_total and dealer_spot < 5 and dealer_total != 21:
            dealer_image1 = dealer_image_1_show
            dealer_label_1.config(image=dealer_image1)
            play_sound("sounds/lose.mp3")
            messagebox.showinfo("Dealer Wins!", "Dealer wins!")
            bet_button.config(state=NORMAL)
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            return
        else:
            if player_total > dealer_total and len(dealer_score) < 5:
                dealer_image1 = dealer_image_1_show
                dealer_label_1.config(image=dealer_image1)
                play_sound("sounds/win.mp3")
                messagebox.showinfo("Player Wins!", "Player Wins!")
                bet_button.config(state=NORMAL)
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                balance += bet_amount * 2
                balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
                return
    else:
        dealer_hit()
        stand()


def blackjack_shuffle(player):
    global balance, bet_amount

    player_total = 0
    dealer_total = 0

    if player == "dealer":
        if len(dealer_score) == 2:
            if dealer_score[0] + dealer_score[1] == 21:
                blackjack_status["dealer"] = "yes"
        else:

            for score in dealer_score:
                dealer_total += score

            if dealer_total == 21:
                blackjack_status["dealer"] = "yes"

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

    if player == "player":
        if len(player_score) == 2:
            if player_score[0] + player_score[1] == 21:
                blackjack_status["player"] = "yes"

        else:
            for score in player_score:
                player_total += score

            if player_total == 21:
                blackjack_status["player"] = "yes"

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

                    if player_total > 21:
                        blackjack_status["player"] = "bust"

    if len(dealer_score) == 2 and len(player_score) == 2:
        if blackjack_status["dealer"] == "yes" and blackjack_status["player"] == "yes":
            dealer_image1 = dealer_image_1_show
            dealer_label_1.config(image=dealer_image1)
            messagebox.showinfo("Push!", "Push: It's a Tie!")
            balance += bet_amount
            balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
            bet_button.config(state=NORMAL)
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            return

        elif blackjack_status["dealer"] == "yes":
            dealer_image1 = dealer_image_1_show
            dealer_label_1.config(image=dealer_image1)
            balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
            play_sound("sounds/lose.mp3")
            messagebox.showinfo("Blackjack!", "Blackjack: Dealer Wins!")
            bet_button.config(state=NORMAL)
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            return

        elif blackjack_status["player"] == "yes":
            dealer_image1 = dealer_image_1_show
            dealer_label_1.config(image=dealer_image1)
            balance += bet_amount * 2.5
            balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
            play_sound("sounds/win.mp3")
            messagebox.showinfo("Blackjack!", "Blackjack: Player Wins!")
            bet_button.config(state=NORMAL)
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            return

    else:
        if blackjack_status["dealer"] == "yes" and blackjack_status["player"] == "yes":
            dealer_image1 = dealer_image_1_show
            dealer_label_1.config(image=dealer_image1)
            messagebox.showinfo("Push!", "Push: It's a Tie!")
            bet_button.config(state=NORMAL)
            card_button.config(state=DISABLED)
            stand_button.config(state=DISABLED)
            balance += bet_amount
            balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
            return

        elif blackjack_status["dealer"] == "yes":
            if len(dealer_score) > 2:
                dealer_image1 = dealer_image_1_show
                dealer_label_1.config(image=dealer_image1)
                play_sound("sounds/lose.mp3")
                messagebox.showinfo("Blackjack", "21: Dealer Wins!")
                balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
                bet_button.config(state=NORMAL)
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                return

        elif blackjack_status["player"] == "yes":
            if len(player_score) > 2:
                while sum(dealer_score) < 17:
                    dealer_hit()
                if player_total > dealer_total and dealer_total < 22:
                    dealer_image1 = dealer_image_1_show
                    dealer_label_1.config(image=dealer_image1)
                    balance += bet_amount * 2
                    play_sound("sounds/win.mp3")
                    messagebox.showinfo("Player wins!", "21!: Player wins!")
                    balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
                    card_button.config(state=DISABLED)
                    stand_button.config(state=DISABLED)
                    bet_button.config(state=NORMAL)
                    return

        elif blackjack_status["player"] == "yes" and sum(dealer_score) >= 17 and sum(dealer_score) != 21:
            if len(player_score) > 2:
                dealer_image1 = dealer_image_1_show
                dealer_label_1.config(image=dealer_image1)
                play_sound("sounds/win.mp3")
                balance += bet_amount * 2
                messagebox.showinfo("21!", "21!: Player wins!")
                balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)
                return
        elif blackjack_status["player"] == "yes" and sum(dealer_score) == 21:
            if len(player_score) > 2:
                dealer_image1 = dealer_image_1_show
                dealer_label_1.config(image=dealer_image1)
                balance += bet_amount
                messagebox.showinfo("Push!", "Push: It's a tie!")
                balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)
                return

    if blackjack_status["player"] == "bust":
        dealer_image1 = dealer_image_1_show
        dealer_label_1.config(image=dealer_image1)
        play_sound("sounds/lose.mp3")
        messagebox.showinfo("Bust!", "Player Busts!")
        bet_button.config(state=NORMAL)
        card_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        return


def resize_cards(card):
    our_card_image_temp = Image.open(card)
    our_card_resize = our_card_image_temp.resize((150, 218))
    our_card_image = ImageTk.PhotoImage(our_card_resize)
    return our_card_image


def shuffle():
    global blackjack_status, player_total, dealer_total, card_button, stand_button
    global dealer, player, dealer_spot, player_spot, dealer_score, player_score, deck

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

    if balance == 0 and dealer_spot > 2 or player_spot > 2:
        messagebox.showinfo(
            "Insufficient Funds", "You don't have enough funds to play!"
        )
        quit()


def dealer_hit():
    global dealer_spot, player_total, dealer_total, player_score, dealer_image_1_show
    global dealer_image1, dealer_image2, dealer_image3, dealer_image4, dealer_image5

    if dealer_spot <= 5 and dealer_total < 17:
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
            dealer_image1 = resize_cards("cards/hidden.png")
            dealer_image_1_show = resize_cards(f"cards/{dealer_card}.png")
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

            if dealer_total < 21 and blackjack_status["player"] != "blackjack":
                dealer_image1 = dealer_image_1_show
                dealer_label_1.config(image=dealer_image1)
                play_sound("sounds/lose.mp3")
                messagebox.showinfo("Dealer wins!", "Dealer wins!")
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)
                return
            elif dealer_total == 21 and blackjack_status["player"] == "blackjack":
                dealer_image1 = dealer_image_1_show
                dealer_label_1.config(image=dealer_image1)
                messagebox.showinfo("Push!", "Push: It's a tie!")
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)
                return

    blackjack_shuffle("dealer")


def player_hit():
    global player_spot, balance, bet_amount, player_image1, player_image2, player_image3, player_image4, player_image5

    if player_spot <= 5:
        player_card = r.choice(deck)
        deck.remove(player_card)
        player.append(player_card)
        pcard = int(player_card.split("_", 1)[0])
        if pcard == 14:
            player_score.append(11)
            if sum(player_score) > 21:
                for card_num, card in enumerate(player_score):
                    if card == 11:
                        player_score[card_num] = 1
                        if sum(player_score) > 21:
                            blackjack_status["player"] = "bust"
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
                dealer_image1 = dealer_image_1_show
                dealer_label_1.config(image=dealer_image1)
                balance += bet_amount * 2
                play_sound("sounds/win.mp3")
                balance_label.config(text=f"Balance: ${balance:.2f}", bg="green")
                messagebox.showinfo("Player wins!", "Player Wins!")
                card_button.config(state=DISABLED)
                stand_button.config(state=DISABLED)
                bet_button.config(state=NORMAL)
                return

    blackjack_shuffle("player")


def deal_cards():

    card = r.choice(deck)
    deck.remove(card)
    dealer.append(card)

    card = r.choice(deck)
    deck.remove(card)
    player.append(card)


my_frame = Frame(root, bg="green")
my_frame.pack(pady=25)

dealer_frame = LabelFrame(
    my_frame, text=" Dealer's Hand ", bd=0, bg="green", labelanchor="n"
)
dealer_frame.pack(padx=20, ipadx=20)

player_frame = LabelFrame(
    my_frame, text=" Player's Hand ", bd=0, bg="green", labelanchor="n"
)
player_frame.pack(ipadx=20, pady=10)

dealer_label_1 = Label(dealer_frame, text="", bg="green")
dealer_label_1.grid(row=0, column=0, pady=20, padx=20)

dealer_label_2 = Label(dealer_frame, text="", bg="green")
dealer_label_2.grid(row=0, column=1, pady=20, padx=20)

dealer_label_3 = Label(dealer_frame, text="", bg="green")
dealer_label_3.grid(row=0, column=2, pady=20, padx=20)

dealer_label_4 = Label(dealer_frame, text="", bg="green")
dealer_label_4.grid(row=0, column=3, pady=20, padx=20)

dealer_label_5 = Label(dealer_frame, text="", bg="green")
dealer_label_5.grid(row=0, column=4, pady=20, padx=20)

player_label_1 = Label(player_frame, text="", bg="green")
player_label_1.grid(row=1, column=0, pady=20, padx=20)

player_label_2 = Label(player_frame, text="", bg="green")
player_label_2.grid(row=1, column=1, pady=20, padx=20)

player_label_3 = Label(player_frame, text="", bg="green")
player_label_3.grid(row=1, column=2, pady=20, padx=20)

player_label_4 = Label(player_frame, text="", bg="green")
player_label_4.grid(row=1, column=3, pady=20, padx=20)

player_label_5 = Label(player_frame, text="", bg="green")
player_label_5.grid(row=1, column=4, pady=20, padx=20)

money_frame = Frame(root, bg="green")
money_frame.pack(
    side=TOP,
    pady=10,
)

balance_label = Label(money_frame, text=f"Balance: ${balance:.2f}", bg="green")
balance_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")


deposit_button = Button(
    money_frame,
    text="Deposit",
    highlightbackground="green",
    highlightcolor="green",
    command=deposit,
)
deposit_button.grid(row=2, column=0, pady=10, sticky="e")

bet_button = Button(
    money_frame,
    text="Bet",
    highlightbackground="green",
    highlightcolor="green",
    command=bet,
    state=DISABLED,
)
bet_button.grid(row=2, column=1, pady=10, sticky="w")

button_frame = Frame(root, bg="green")
button_frame.pack(side=BOTTOM, pady=15)

card_button = Button(
    button_frame,
    text="Hit",
    bg="green",
    font=("Arial", 15),
    command=player_hit,
    padx=20,
    pady=10,
    highlightbackground="green",
)


stand_button = Button(
    button_frame,
    text="Stand",
    bg="green",
    font=("Arial", 15),
    command=stand,
    padx=20,
    pady=10,
    highlightbackground="green",
)


root.mainloop()

from tkinter import *
from tkinter import messagebox
import random as r
from PIL import ImageTk, Image

root = Tk()
root.title("Blackjack")
root.iconbitmap("cards/icon.png")
root.geometry("1200x800")
root.configure(bg="green")


def blackjack_shuffle(player):
    global player_total, dealer_total, player_score

    player_total = 0
    dealer_total = 0
    if player == "dealer":
        if len(dealer_score) == 2:
            if dealer_score[0] + dealer_score[1] == 21:

                blackjack_status["dealer"] = "yes"

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

            messagebox.showinfo("Push!", "Push: It's a Tie!")
            card_button.config(state="disabled")
            stand_button.config(state="disabled")
            double_button.config(state="disabled")

        elif blackjack_status["dealer"] == "yes":
            messagebox.showinfo("Blackjack!", "Blackjack: Dealer Wins!")

            card_button.config(state="disabled")
            stand_button.config(state="disabled")
            double_button.config(state="disabled")


        elif blackjack_status["player"] == "yes":
            messagebox.showinfo("Blackjack!", "Blackjack: Player Wins!")

            card_button.config(state="disabled")
            stand_button.config(state="disabled")
            double_button.config(state="disabled")
    else:

        if blackjack_status["dealer"] == "yes" and blackjack_status["player"] == "yes":

            messagebox.showinfo("Push!", "Push: It's a Tie!")
            card_button.config(state="disabled")
            stand_button.config(state="disabled")
            double_button.config(state="disabled")

        elif blackjack_status["dealer"] == "yes":
            if len(dealer_score) > 2:
                messagebox.showinfo("21!", "21: Dealer Wins!")
                card_button.config(state="disabled")
                stand_button.config(state="disabled")
                double_button.config(state="disabled")

        elif blackjack_status["player"] == "yes":
            if len(player_score) > 2:
                messagebox.showinfo("21!", "21: Player Wins!")
                card_button.config(state="disabled")
                stand_button.config(state="disabled")
                double_button.config(state="disabled")

    if blackjack_status["player"] == "bust":
        messagebox.showinfo("Player Busts!", f"Player Loses! {player_total}")

        card_button.config(state="disabled")
        stand_button.config(state="disabled")


def resize_cards(card):
    global our_card_image
    our_card_image = Image.open(card)

    our_card_resize = our_card_image.resize((150, 218))

    our_card_image = ImageTk.PhotoImage(our_card_resize)
    return our_card_image


def shuffle():
    global blackjack_status, player_total, dealer_total

    player_total = 0
    dealer_total = 0

    blackjack_status = {"dealer": "no", "player": "no"}

    card_button.config(state="normal")
    stand_button.config(state="normal")
    double_button.config(state="normal")

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

    global deck
    deck = []
    for suit in suits:
        for value in values:
            deck.append(f"{value}_of_{suit}")


    global dealer, player, dealer_spot, player_spot, dealer_score, player_score
    dealer = []
    player = []
    dealer_score = []
    player_score = []
    dealer_spot = 0
    player_spot = 0

    for _ in range(2):
        player_hit()
        dealer_hit()

    root.title(f"Blackjack | Cards left: {len(deck)}")


def dealer_hit():
    global dealer_spot
    if dealer_spot < 5:
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

            global dealer_image1, dealer_image2, dealer_image3, dealer_image4, dealer_image5

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

            root.title(f"Blackjack | Cards left: {len(deck)}")

        except:
            root.title("Blackjack | Cards left: 0")

        blackjack_shuffle("dealer")


def player_hit():
    global player_spot
    if player_spot < 5:
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

            global player_image1, player_image2, player_image3, player_image4, player_image5

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

            root.title(f"Blackjack | Cards left: {len(deck)}")

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

        root.title(f"Blackjack | Cards left: {len(deck)}")

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

button_frame = Frame(root, bg='green')
button_frame.pack(pady=20)

shuffle_button = Button(button_frame, text="Shuffle", font=("Arial", 15), command=shuffle)
shuffle_button.grid(row=0, column=0)

card_button = Button(button_frame, text="Hit", font=("Arial", 15), command=player_hit)
card_button.grid(row=0, column=1, padx=10)

stand_button = Button(button_frame, text="Stand", font=("Arial", 15))
stand_button.grid(row=0, column=2, padx=10)

double_button = Button(button_frame, text="Double Down", font=("Arial", 15))
double_button.grid(row=0, column=3)
shuffle()

root.mainloop()

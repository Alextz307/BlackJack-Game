"""
    A program that simulates a simple BlackJack game between one used and a dealer.
"""


from random import shuffle


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 
'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card: 
    """
        Holds information about a single game card.
    """
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]


    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    """
        Holds information about a deck of cards.
    """

    def __init__(self):
        cards = []

        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                cards.append(card)

        self.cards = cards


    def __str__(self):
        deck_comp = ''

        for card in self.cards:
            deck_comp += '\n' + str(card)


        return 'The deck has:' + deck_comp


    def __len__(self):
        return len(self.cards)


    def shuffle_deck(self):
        """
            Shuffle the deck.
        """

        shuffle(self.cards)


    def deal(self):
        """
            Deal a card from the deck and return that card.
        """

        return self.cards.pop(0)


class BankAccount:
    """
        Holds information about a player's balance.
    """

    def __init__(self, balance):
        self.balance = balance


    def __str__(self):
        return f'Your account balance is {self.balance}$'


    def withdraw(self, req):
        """
            Method for withdrawing money from the account.
        """

        if self.balance < req:
            print('You do not have enough funds!')
            return False

        self.balance -= req
        return True


    def deposit(self, money):
        """
            Method for depositing money in the account.
        """

        self.balance += money


class Hand:
    """
        Holds information about a player's hand in BlackJack.
    """

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0


    def __str__(self):
        return f"Hand's value is {self.value}"


    def add_card(self, card):
        """
            Add a card to a hand and update the hand's value.
        """

        self.cards.append(card)
        self.value += card.value
        self.aces += (card.rank == 'Ace')

        # Adjust aces
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


    def bust(self):
        """
            Checks for a bust using the value attribute.
        """

        return self.value > 21


class Player(BankAccount):
    """
        Holds relevant information about a BlackJack player.
    """

    def __init__(self, name, money):
        BankAccount.__init__(self, money)
        self.name = name
        self.hand = Hand()


def retrieve_sum_of_money(message, name):
    """
        Request the user for a positive integer sum of money.
    """

    while True:
        try:
            money = int(input(f'{name}, please enter your {message}, which should be a positive integer value! '))
        except ValueError:
            print('You did not enter an integer value, please enter another value!')
        else:
            if money <= 0:
                print('You did not enter a positive value, please enter another value!')
            else:
                return money


def retrieve_answer(message, option1, option2, valid_answers):
    """
        Request for a specific answer.
    """

    while True:
        answer = input(message + f' Enter {option1} or {option2}. ')

        if answer.lower() not in valid_answers:
            print(f'You did not answer with {option1} or {option2}. Please answer again.')
        else:
            return answer.lower()


def make_bet(player):
    """
        Function for placing a bet.
    """

    while True:
        bet = retrieve_sum_of_money('bet', player.name)

        if player.withdraw(bet):
            return player, bet


def main():
    """
        Main function for simulating the actual game.
    """

    print("Welcome to Royale Casino! Let's play some BlackJack!")

    name = input('Please enter your name! ')

    money = retrieve_sum_of_money('money deposit', name)

    player = Player(name, money)

    while True:
        print(player)

        print("Let's shuffle the deck of cards!")
        deck = Deck()
        deck.shuffle_deck()

        player, bet = make_bet(player)

        print('Dealing cards...')

        player.hand = Hand()

        for _ in range(2):
            player.hand.add_card(deck.deal())

        dealer_hand = Hand()

        for _ in range(2):
            dealer_hand.add_card(deck.deal())

        print("One of the dealer's cards is " + str(dealer_hand.cards[1]))

        print(f"{player.name}'s first card is " + str(player.hand.cards[0]))
        print(f"{player.name}'s second card is " + str(player.hand.cards[1]))

        while True:
            option = retrieve_answer(f'{name}, do you hit or stand?', 'hit', 'stand', ['hit', 'stand'])

            if option == 'stand':
                break

            player.hand.add_card(deck.deal())
            print('You got ' + str(player.hand.cards[-1]))

            if player.hand.bust():
                print(f'{player.name}, you busted!')
                break


        if not player.hand.bust():
            print('The other card of the dealer is ' + str(dealer_hand.cards[0]))

            while dealer_hand.value < 17:
                dealer_hand.add_card(deck.deal())
                print('Dealer received ' + str(dealer_hand.cards[-1]))


            if dealer_hand.bust() or dealer_hand.value < player.hand.value:
                print(f'Congratulations, {player.name}, you won!')
                player.deposit(2 * bet)
            elif dealer_hand.value == player.hand.value:
                print('This round resulted in a tie, so you get your money back!')
                player.deposit(bet)
            else:
                print('You lost!')


        option = retrieve_answer(f'{name}, do you want to continue playing?', 'yes', 'no', ['y', 'yes', 'n', 'no'])

        if option[0] == 'n':
            break


        if player.balance == 0:
            option = retrieve_answer(f'{name}, you do not have any money left. Do you want to make a deposit in order to continue playing', 
                'yes', 'no', ['y', 'yes', 'n', 'no'])
        
            if option[0] == 'n':
                break

            money = retrieve_sum_of_money('money deposit', name)
            player.deposit(money)

            print('All good, now you can continue playing!')
        

    print(f'Thank you for playing! You can withdraw your credits, which value {player.balance}$!')
    player.withdraw(player.balance)


if __name__ == '__main__':
    main()

from __future__ import annotations
import random
from typing import Optional, List, Dict, Tuple

import discord
from discord import Member, app_commands

from imp.utils import strict_types
from views.request_match import RequestMatch
from views.game import GameInitView, GameView, GameStopView

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imp.better import BetterBot, BetterInteraction

class CardEnum:
    NONE = None

class CardColors(CardEnum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    BLACK = "BLACK"

class CardNumbers(CardEnum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

class CardAbilities(CardEnum):
    WISH = "WISH"
    TRADE_ALL = "TRADE ALL"
    PLUS_TWO = "+2"
    PLUS_FOUR = "+4"
    SKIP_NEXT = "SKIP"
    REVERSE_ORDER = "REVERSE"

class Card:
    def __init__(self, color: str, number: int, ability: str, name: str = None):
        self.color: str = color
        self.number: int = number
        self.ability: str = ability

        self.name: str = name

    def matches_color(self, color: str):
        return self.color == color

    def matches_number(self, number: int):
        return self.number == number

    def has_ability(self, ability: Tuple[int, str]):
        return self.ability == ability

class CardTransformer(app_commands.Transformer):
    @staticmethod
    async def transform(interaction: BetterInteraction, value: str) -> Optional[Card]:
        m = interaction.client.game_manager
        if not m.is_player(interaction.user):
            return None

        game = m.get_player_game(interaction.user)
        par = game.get_participant(interaction.user)

        c = ([c for c in par.stack.cards if c.name == value] or [None])[0]
        if c is None:
            await interaction.response.send_message(
                content="You don't have this card",
                ephemeral=True
            )
        return c


class CardTypes:
    BLUE_ZERO = Card(CardColors.BLUE, CardNumbers.ZERO, CardAbilities.NONE, "BLUE ZERO")  # x1
    BLUE_ONE = Card(CardColors.BLUE, CardNumbers.ONE, CardAbilities.NONE, "BLUE ONE")  # x2
    BLUE_TWO = Card(CardColors.BLUE, CardNumbers.TWO, CardAbilities.NONE, "BLUE TWO")  # x2
    BLUE_THREE = Card(CardColors.BLUE, CardNumbers.THREE, CardAbilities.NONE, "BLUE THREE")  # x2
    BLUE_FOUR = Card(CardColors.BLUE, CardNumbers.FOUR, CardAbilities.NONE, "BLUE FOUR")  # x2
    BLUE_FIVE = Card(CardColors.BLUE, CardNumbers.FIVE, CardAbilities.NONE, "BLUE FIVE")  # x2
    BLUE_SIX = Card(CardColors.BLUE, CardNumbers.SIX, CardAbilities.NONE, "BLUE SIX")  # x2
    BLUE_SEVEN = Card(CardColors.BLUE, CardNumbers.SEVEN, CardAbilities.NONE, "BLUE SEVEN")  # x2
    BLUE_EIGHT = Card(CardColors.BLUE, CardNumbers.EIGHT, CardAbilities.NONE, "BLUE EIGHT")  # x2
    BLUE_NINE = Card(CardColors.BLUE, CardNumbers.NINE, CardAbilities.NONE, "BLUE NINE")  # x2
    BLUE_SKIP = Card(CardColors.BLUE, CardNumbers.NONE, CardAbilities.SKIP_NEXT, "BLUE SKIP")  # x2
    BLUE_PLUS_TWO = Card(CardColors.BLUE, CardNumbers.NONE, CardAbilities.PLUS_TWO, "BLUE +2")  # x2
    BLUE_REVERSE = Card(CardColors.BLUE, CardNumbers.NONE, CardAbilities.REVERSE_ORDER, "BLUE REVERSE")  # x2

    RED_ZERO = Card(CardColors.RED, CardNumbers.ZERO, CardAbilities.NONE, "RED ZERO")  # x1
    RED_ONE = Card(CardColors.RED, CardNumbers.ONE, CardAbilities.NONE, "RED ONE")  # x2
    RED_TWO = Card(CardColors.RED, CardNumbers.TWO, CardAbilities.NONE, "RED TWO")  # x2
    RED_THREE = Card(CardColors.RED, CardNumbers.THREE, CardAbilities.NONE, "RED THREE")  # x2
    RED_FOUR = Card(CardColors.RED, CardNumbers.FOUR, CardAbilities.NONE, "RED FOUR")  # x2
    RED_FIVE = Card(CardColors.RED, CardNumbers.FIVE, CardAbilities.NONE, "RED FIVE")  # x2
    RED_SIX = Card(CardColors.RED, CardNumbers.SIX, CardAbilities.NONE, "RED SIX")  # x2
    RED_SEVEN = Card(CardColors.RED, CardNumbers.SEVEN, CardAbilities.NONE, "RED SEVEN")  # x2
    RED_EIGHT = Card(CardColors.RED, CardNumbers.EIGHT, CardAbilities.NONE, "RED EIGHT")  # x2
    RED_NINE = Card(CardColors.RED, CardNumbers.NINE, CardAbilities.NONE, "RED NINE")  # x2
    RED_SKIP = Card(CardColors.RED, CardNumbers.NONE, CardAbilities.SKIP_NEXT, "RED SKIP")  # x2
    RED_PLUS_TWO = Card(CardColors.RED, CardNumbers.NONE, CardAbilities.PLUS_TWO, "RED +2")  # x2
    RED_REVERSE = Card(CardColors.RED, CardNumbers.NONE, CardAbilities.REVERSE_ORDER, "RED REVERSE")  # x2

    GREEN_ZERO = Card(CardColors.GREEN, CardNumbers.ZERO, CardAbilities.NONE, "GREEN ZERO")  # x1
    GREEN_ONE = Card(CardColors.GREEN, CardNumbers.ONE, CardAbilities.NONE, "GREEN ONE")  # x2
    GREEN_TWO = Card(CardColors.GREEN, CardNumbers.TWO, CardAbilities.NONE, "GREEN TWO")  # x2
    GREEN_THREE = Card(CardColors.GREEN, CardNumbers.THREE, CardAbilities.NONE, "GREEN THREE")  # x2
    GREEN_FOUR = Card(CardColors.GREEN, CardNumbers.FOUR, CardAbilities.NONE, "GREEN FOUR")  # x2
    GREEN_FIVE = Card(CardColors.GREEN, CardNumbers.FIVE, CardAbilities.NONE, "GREEN FIVE")  # x2
    GREEN_SIX = Card(CardColors.GREEN, CardNumbers.SIX, CardAbilities.NONE, "GREEN SIX")  # x2
    GREEN_SEVEN = Card(CardColors.GREEN, CardNumbers.SEVEN, CardAbilities.NONE, "GREEN SEVEN")  # x2
    GREEN_EIGHT = Card(CardColors.GREEN, CardNumbers.EIGHT, CardAbilities.NONE, "GREEN EIGHT")  # x2
    GREEN_NINE = Card(CardColors.GREEN, CardNumbers.NINE, CardAbilities.NONE, "GREEN NINE")  # x2
    GREEN_SKIP = Card(CardColors.GREEN, CardNumbers.NONE, CardAbilities.SKIP_NEXT, "GREEN SKIP")  # x2
    GREEN_PLUS_TWO = Card(CardColors.GREEN, CardNumbers.NONE, CardAbilities.PLUS_TWO, "GREEN +2")  # x2
    GREEN_REVERSE = Card(CardColors.GREEN, CardNumbers.NONE, CardAbilities.REVERSE_ORDER, "GREEN REVERSE")  # x2

    YELLOW_ZERO = Card(CardColors.YELLOW, CardNumbers.ZERO, CardAbilities.NONE, "YELLOW ZERO")  # x1
    YELLOW_ONE = Card(CardColors.YELLOW, CardNumbers.ONE, CardAbilities.NONE, "YELLOW ONE")  # x2
    YELLOW_TWO = Card(CardColors.YELLOW, CardNumbers.TWO, CardAbilities.NONE, "YELLOW TWO")  # x2
    YELLOW_THREE = Card(CardColors.YELLOW, CardNumbers.THREE, CardAbilities.NONE, "YELLOW THREE")  # x2
    YELLOW_FOUR = Card(CardColors.YELLOW, CardNumbers.FOUR, CardAbilities.NONE, "YELLOW FOUR")  # x2
    YELLOW_FIVE = Card(CardColors.YELLOW, CardNumbers.FIVE, CardAbilities.NONE, "YELLOW FIVE")  # x2
    YELLOW_SIX = Card(CardColors.YELLOW, CardNumbers.SIX, CardAbilities.NONE, "YELLOW SIX")  # x2
    YELLOW_SEVEN = Card(CardColors.YELLOW, CardNumbers.SEVEN, CardAbilities.NONE, "YELLOW SEVEN")  # x2
    YELLOW_EIGHT = Card(CardColors.YELLOW, CardNumbers.EIGHT, CardAbilities.NONE, "YELLOW EIGHT")  # x2
    YELLOW_NINE = Card(CardColors.YELLOW, CardNumbers.NINE, CardAbilities.NONE, "YELLOW NINE")  # x2
    YELLOW_SKIP = Card(CardColors.YELLOW, CardNumbers.NONE, CardAbilities.SKIP_NEXT, "YELLOW SKIP")  # x2
    YELLOW_PLUS_TWO = Card(CardColors.YELLOW, CardNumbers.NONE, CardAbilities.PLUS_TWO, "YELLOW +2")  # x2
    YELLOW_REVERSE = Card(CardColors.YELLOW, CardNumbers.NONE, CardAbilities.REVERSE_ORDER, "YELLOW REVERSE")  # x2

    BLACK_WISH = Card(CardColors.BLACK, CardNumbers.NONE, CardAbilities.WISH, "BLACK WISH")         # x4
    BLACK_PLUS_FOUR = Card(CardColors.BLACK, CardNumbers.NONE, CardAbilities.PLUS_FOUR, "BLACK +4") # x4
    BLACK_TRADE_ALL = Card(CardColors.BLACK, CardNumbers.NONE, CardAbilities.TRADE_ALL, "BLACK TRADE")  # x1


AllCards = [
    CardTypes.BLUE_ZERO,
    CardTypes.BLUE_ONE, CardTypes.BLUE_ONE,
    CardTypes.BLUE_TWO, CardTypes.BLUE_TWO,
    CardTypes.BLUE_THREE, CardTypes.BLUE_THREE,
    CardTypes.BLUE_FOUR, CardTypes.BLUE_FOUR,
    CardTypes.BLUE_FIVE, CardTypes.BLUE_FIVE,
    CardTypes.BLUE_SIX, CardTypes.BLUE_SIX,
    CardTypes.BLUE_SEVEN, CardTypes.BLUE_SEVEN,
    CardTypes.BLUE_EIGHT, CardTypes.BLUE_EIGHT,
    CardTypes.BLUE_NINE, CardTypes.BLUE_NINE,
    CardTypes.BLUE_SKIP, CardTypes.BLUE_SKIP,
    CardTypes.BLUE_REVERSE, CardTypes.BLUE_REVERSE,
    CardTypes.BLUE_PLUS_TWO, CardTypes.BLUE_PLUS_TWO,

    CardTypes.RED_ZERO,
    CardTypes.RED_ONE, CardTypes.RED_ONE,
    CardTypes.RED_TWO, CardTypes.RED_TWO,
    CardTypes.RED_THREE, CardTypes.RED_THREE,
    CardTypes.RED_FOUR, CardTypes.RED_FOUR,
    CardTypes.RED_FIVE, CardTypes.RED_FIVE,
    CardTypes.RED_SIX, CardTypes.RED_SIX,
    CardTypes.RED_SEVEN, CardTypes.RED_SEVEN,
    CardTypes.RED_EIGHT, CardTypes.RED_EIGHT,
    CardTypes.RED_NINE, CardTypes.RED_NINE,
    CardTypes.RED_SKIP, CardTypes.RED_SKIP,
    CardTypes.RED_REVERSE, CardTypes.RED_REVERSE,
    CardTypes.RED_PLUS_TWO, CardTypes.RED_PLUS_TWO,

    CardTypes.GREEN_ZERO,
    CardTypes.GREEN_ONE, CardTypes.GREEN_ONE,
    CardTypes.GREEN_TWO, CardTypes.GREEN_TWO,
    CardTypes.GREEN_THREE, CardTypes.GREEN_THREE,
    CardTypes.GREEN_FOUR, CardTypes.GREEN_FOUR,
    CardTypes.GREEN_FIVE, CardTypes.GREEN_FIVE,
    CardTypes.GREEN_SIX, CardTypes.GREEN_SIX,
    CardTypes.GREEN_SEVEN, CardTypes.GREEN_SEVEN,
    CardTypes.GREEN_EIGHT, CardTypes.GREEN_EIGHT,
    CardTypes.GREEN_NINE, CardTypes.GREEN_NINE,
    CardTypes.GREEN_SKIP, CardTypes.GREEN_SKIP,
    CardTypes.GREEN_REVERSE, CardTypes.GREEN_REVERSE,
    CardTypes.GREEN_PLUS_TWO, CardTypes.GREEN_PLUS_TWO,

    CardTypes.YELLOW_ZERO,
    CardTypes.YELLOW_ONE, CardTypes.YELLOW_ONE,
    CardTypes.YELLOW_TWO, CardTypes.YELLOW_TWO,
    CardTypes.YELLOW_THREE, CardTypes.YELLOW_THREE,
    CardTypes.YELLOW_FOUR, CardTypes.YELLOW_FOUR,
    CardTypes.YELLOW_FIVE, CardTypes.YELLOW_FIVE,
    CardTypes.YELLOW_SIX, CardTypes.YELLOW_SIX,
    CardTypes.YELLOW_SEVEN, CardTypes.YELLOW_SEVEN,
    CardTypes.YELLOW_EIGHT, CardTypes.YELLOW_EIGHT,
    CardTypes.YELLOW_NINE, CardTypes.YELLOW_NINE,
    CardTypes.YELLOW_SKIP, CardTypes.YELLOW_SKIP,
    CardTypes.YELLOW_REVERSE, CardTypes.YELLOW_REVERSE,
    CardTypes.YELLOW_PLUS_TWO, CardTypes.YELLOW_PLUS_TWO,

    CardTypes.BLACK_PLUS_FOUR, CardTypes.BLACK_PLUS_FOUR, CardTypes.BLACK_PLUS_FOUR, CardTypes.BLACK_PLUS_FOUR,
    CardTypes.BLACK_WISH, CardTypes.BLACK_WISH, CardTypes.BLACK_WISH, CardTypes.BLACK_WISH,
    CardTypes.BLACK_TRADE_ALL
]

class CardInventory:
    def __init__(self, holder: Member):
        self.holder = holder
        self.cards: List[Card] = []

    @strict_types
    def add_card(self, *card: Card):
        self.cards += list(card)

    @strict_types
    def remove_card(self, card: Card):
        self.cards.remove(card)

class Participant:
    def __init__(self, user: Member):
        self.user: Member = user
        self.stack: CardInventory = CardInventory(user)
        self.took_card: bool = False

    def has_no_cards(self) -> bool:
        return len(self.stack.cards) == 0

    @classmethod
    def from_user(cls, user: Member):
        return cls(user)

    @strict_types
    def give_card(self, *card: Card):
        self.stack.add_card(*card)

    @strict_types
    def remove_card(self, card: Card):
        self.stack.remove_card(card)

    def __str__(self) -> str:
        return str(self.user)


class StackedCard:
    def __init__(self, card: Card, placer: Participant):
        self.card: Optional[Card] = card
        self.placer: Optional[Participant] = placer

    @strict_types
    def is_compatible(self, card: Card) -> bool:
        # if card.color == CardColors.BLACK:
        #     return True
        #
        # if self.card.color == CardColors.BLACK:
        #     return True
        #
        # return self.card.color == card.color or self.card.number == card.number
        return True

class FirstCard(StackedCard):
    def __init__(self):
        self.card: Optional[Card] = Card(CardColors.NONE, CardNumbers.NONE, CardAbilities.NONE, "First Card")
        self.placer: Optional[Card] = None

    @strict_types
    def is_compatible(self, card: Card) -> bool:
        return True

class CardStack:
    def __init__(self):
        self.cards: List[StackedCard] = [FirstCard()]
        self.unused = AllCards.copy()

    @strict_types
    def lay_card(self, card: Card, participant: Participant):
        if not self.card_layable(card):
            raise ValueError("Card not compatible.")

        self.cards.append(StackedCard(card, participant))

    def unused_count(self):
        return len(self.unused)

    @strict_types
    def card_layable(self, card: Card) -> bool:
        return self.top_card.is_compatible(card)

    @strict_types
    def gen_cards(self, amount: int = 1) -> List[Card]:
        return [self.random_card() for _ in range(amount)]

    def random_card(self) -> Card:
        if len(self.unused) == 0:
            self.unused = [sc.card for sc in self.cards[:-1]]
            # self.cards = self.cards[-1:]

        return self.unused.pop(random.randint(0, len(self.unused)-1))

    @property
    def top_card(self) -> Optional[StackedCard]:
        return self.cards[-1]

class UNOGame:
    def __init__(self, client: BetterBot, host: Member, message: discord.Message):
        self.client = client
        self.host: Member = host
        self.message = message
        self.init_view: Optional[GameInitView] = None
        self.game_view: Optional[GameView] = None
        self.game_stop_view: Optional[GameStopView] = None
        self.participants: Dict[Member, Participant] = {host: Participant(host)}
        self.stack = CardStack()
        self.started: bool = False
        self.pending_invites: Dict[Member, RequestMatch] = {}
        self.turn: int = 0
        self.order: List[Participant] = [self.get_participant(host)]
        self.pending_cards: List[Card] = []
        self.direction = +1
        self.actions: List[str] = []

    def turn_order(self) -> str:
        return "\n".join(
            f"**Now**: {player.user.mention}" if self.turn == turn else f"       **{turn+1}**: {player.user.mention}" for turn, player in enumerate(self.order)
        )

    def gen_desc(
        self,
        show_stats: bool = True,
        show_participants: bool = True,
        show_turn: bool = True,
        show_top_card: bool = True,
        show_info: bool = True,
        buffer: int = 5
    ) -> str:
        stats = f"\
**Card stats**:\n\
**{self.stack.unused_count()}** unused cards left\n\
**{len(self.pending_cards)}** pending cards\n\n\
"
        _participants = "\n".join(p.mention for p in self.participants)
        participants = f"\
**Participants ({self.participant_count()})**:\n\
{_participants}\n\n\
"
        turn = f"\
**Current turn**:\n\
{self.cur_participant().user.mention}\n\n\
"
        top_card = f"\
**Top Card**:\n\
{self.stack.top_card.card.name}\n\n\
"
        _info = "\n".join(self.actions[-buffer:])
        info = f"\
**Info**:\n\
{_info}\
"


        return f"{stats if show_stats else ''}{participants if show_participants else ''}{turn if show_turn else ''}{top_card if show_top_card else ''}{info if show_info else ''}"

    def participant_count(self) -> int:
        return len(self.participants)

    @strict_types
    def give_cards(self, card_count: int = 7):
        for _ in range(card_count):
            for participant in self.participants.values():
                participant.give_card(self.stack.random_card())

    async def init_game_view(self):
        self.tell("**!** Game created")
        await self.message.edit(
            embed=discord.Embed(
                title="UNO-Game",
                description=self.gen_desc(show_stats=False, show_top_card=False, show_turn=False),
                colour=discord.Colour.yellow()
            ),
            view=GameInitView(self.client, self.host)
        )

    async def start(self):
        self.started = True
        self.order = list(self.participants.values())

        random.shuffle(self.order)

        self.give_cards()
        self.tell("**!** Game has started")

        await self.message.edit(
            embed=discord.Embed(
                title="UNO-Game",
                description=self.gen_desc(
                    show_participants=False
                ),
                colour=discord.Colour.green()
            ),
            view=GameView(self.client, self.host)
        )

    async def stop(self, won: Participant = None):
        self.started = False
        if won is not None:
            self.tell(f"{won.user.mention} won the game")

        self.tell("**!** Game has stopped")

        await self.update_message(
            show_stats=False,
            show_turn=False,
            show_top_card=False
        )

        self.game_stop_view = GameStopView(self.client)
        await self.message.edit(
            view=self.game_stop_view
        )
        await self.message.delete(delay=30)

    @strict_types
    def has_participant(self, participant: Member) -> bool:
        return participant in self.participants

    @strict_types
    def add_participant(self, participant: Participant):
        if self.has_participant(participant.user):
            raise ValueError("Participant already exist.")

        self.participants[participant.user] = participant

    @strict_types
    def remove_participant(self, participant: Participant):
        del self.participants[participant.user]

    @strict_types
    def get_participant(self, player: Member) -> Participant:
        if participant := self.participants.get(player):
            return participant
        else:
            raise ValueError("User is not participating.")

    @strict_types
    def set_participant(self, participant: Participant):
        self.participants[participant.user] = participant

    @strict_types
    def is_pending_invite(self, player: Member) -> bool:
        return player in self.pending_invites.keys()

    @strict_types
    def add_pending_invite(
        self,
        player: Member,
        invite: RequestMatch
    ):
        self.pending_invites[player] = invite

    @strict_types
    def remove_pending_invite(self, player: Member, cancel: bool = False):
        invite = self.pending_invites.pop(player)

        if not invite:
            raise ValueError("Invite does not exist.")

        if cancel:
            invite.cancel_invite()


    @strict_types
    def is_turn(self, participant: Participant):
        return self.turn == self.order.index(participant)

    @strict_types
    def next_turn(self, apply: bool = True, direction: int = None) -> int:
        par = self.cur_participant()
        par.took_card = False
        self.set_participant(par)

        if direction is None:
            direction = self.direction

        _turn = self.turn + direction
        pc = self.participant_count() - 1

        if _turn > pc:
            _turn = 0

        if _turn < 0:
            _turn = pc

        if apply:
            self.turn = _turn

        return _turn

    def tell(self, message: str):
        self.actions.append(message)

    async def update_message(
        self,
        show_stats: bool = True,
        show_participants: bool = True,
        show_turn: bool = True,
        show_top_card: bool = True,
        show_info: bool = True,
        buffer: int = 5
    ):
        await self.message.edit(
            embed=discord.Embed(
                title="UNO-Game",
                description=self.gen_desc(
                    show_stats,
                    show_participants,
                    show_turn,
                    show_top_card,
                    show_info,
                    buffer
                ),
                colour=discord.Colour.green()
            )
        )

    def add_pending_cards(self, count: int = 1):
        self.pending_cards += self.stack.gen_cards(count)

    def reverse_order(self) -> int:
        self.direction *= -1
        return self.direction

    def prev_participant(self) -> Participant:
        return self.order[self.next_turn(False, -1)]

    def next_partcipant(self) -> Participant:
        return self.order[self.next_turn(False, 1)]

    def cur_participant(self) -> Participant:
        return self.order[self.turn]

    async def place_card(self, participant: Participant, card: Card):
        given_cards = 0

        participant.remove_card(card)
        self.stack.lay_card(card, participant)


        if card.has_ability(CardAbilities.SKIP_NEXT):
            self.next_turn()

        if card.has_ability(CardAbilities.REVERSE_ORDER):
            self.reverse_order()

        if card.has_ability(CardAbilities.WISH):
            # TODO: implement wish logic
            pass

        if card.has_ability(CardAbilities.TRADE_ALL):
            # TODO: implement trade logic
            pass

        if card.has_ability(CardAbilities.PLUS_TWO):
            self.add_pending_cards(2)

        elif card.has_ability(CardAbilities.PLUS_FOUR):
            self.add_pending_cards(4)

        else:
            pc = len(self.pending_cards)
            if pc > 0:
                participant.give_card(*self.pending_cards)
                given_cards = pc

                self.pending_cards.clear()

        self.next_turn()
        self.set_participant(participant)

        self.tell(
            f"{participant.user.mention} placed a **{card.name}**" if given_cards == 0 else f"{participant.user.mention} placed a **{card.name}** and got **{given_cards}** cards.")

        await self.update_message(
            show_participants=False
        )

    async def draw_card(self, participant: Participant) -> Card:
        card = self.stack.random_card()
        participant.give_card(card)
        participant.took_card = True
        self.set_participant(participant)

        self.tell(f"{participant.user.mention} took a card")
        await self.update_message(
            show_participants=False
        )

        return card

    async def skip(self):
        if len(self.pending_cards) > 0:
            p = self.cur_participant()
            p.give_card(*self.pending_cards)

            self.set_participant(p)

        self.tell(f"{self.cur_participant().user.mention} skipped.")
        self.next_turn()
        await self.update_message(
            show_participants=False
        )


class GameManager:
    def __init__(self, client: BetterBot):
        self.client = client
        self.games: Dict[Member, UNOGame] = {}
        self.current_hosts: List[Member] = []

    async def skip_participant(self, game: UNOGame):
        await game.skip()
        self.set_game(game.host, game)

    async def draw_card(self, game: UNOGame, participant: Participant) -> Card:
        card = await game.draw_card(participant)
        self.set_game(game.host, game)
        return card

    @strict_types
    def is_host(
        self,
        user: Member
    ) -> bool:
        return user in self.current_hosts

    @strict_types
    def is_player(
        self,
        player: Member
    ) -> bool:
        return any(game.has_participant(player) for game in self.games.values())

    @strict_types
    def get_game(
        self,
        host: Member
    ) -> UNOGame:
        if not self.is_host(host):
            raise ValueError("This is not a host.")

        return self.games.get(host)

    @strict_types
    def set_game(
        self,
        host: Member,
        game: UNOGame
    ):
        self.games[host] = game

    @strict_types
    def get_player_game(
        self,
        player: Member
    ) -> UNOGame:
        return next(game for game in self.games.values() if game.has_participant(player))

    @strict_types
    async def create_game(
        self,
        host: Member,
        message: discord.Message
    ) -> UNOGame:
        if self.is_host(host):
            raise ValueError("This host already has a game running!")

        if self.is_player(host):
            raise ValueError("This user is already in a game!")

        game = UNOGame(self.client, host, message)
        await game.init_game_view()

        self.current_hosts.append(host)
        self.games[host] = game

        return game

    @strict_types
    async def stop_game(self, host: Member, won: Participant = None) -> UNOGame:
        if not self.is_host(host):
            raise ValueError("User is not host of any game")

        game: UNOGame = self.get_game(host)
        await game.stop(won=won)
        del self.games[host]
        self.current_hosts.remove(host)

        return game

    @strict_types
    async def start_game(self, host: Member) -> UNOGame:
        if not self.is_host(host):
            raise ValueError("User is not host of any game")

        game: UNOGame = self.get_game(host)
        await game.start()
        self.set_game(host, game)
        return game

    @strict_types
    async def report_card(self, participant: Participant) -> StackedCard:
        # TODO: report logic
        game = self.get_player_game(participant.user)
        return game.stack.cards[-1]

    @strict_types
    async def place_card(self, game: UNOGame, participant: Participant, card: Card):
        await game.place_card(participant, card)

        self.set_game(game.host, game)

import random
from typing import List, Optional

import discord
from discord.ext import commands

from src.bot.cogs._base import BaseCog


class RussianRouletteView(discord.ui.View):
    CHAMBER_SLOTS = 6
    BULLETS_LOADED = 1

    def __init__(self, players: List[discord.Member], timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)

        random.shuffle(players)
        self.players: List[discord.Member] = players

        self.bullet_location: int = self.generate_bullet_position()
        self.current_chamber: int = 1
        self.blank_shots_in_a_row: int = 0

        self.rounds_played: int = 0
        self.current_player: discord.Member = self.get_next_player()
        self._create_embed()

    # region Embed
    def _create_embed(self) -> None:
        """Creates initial game embed."""

        embed = discord.Embed(title='Russian Roulette', colour=discord.Color.blue())
        embed.add_field(
            name='Player list',
            value=' \n'.join(player.mention for player in self.players),
        )
        embed.add_field(
            name='Placeholder',
            value='Player should not see this',
            inline=False,
        )
        self.game_embed = embed
        self._set_embed_next_round()

    def _set_embed_next_round(self) -> None:
        """Updates embed for next round scenario."""

        self.game_embed.set_thumbnail(url=f'{self.current_player.avatar.url}')
        self.game_embed.set_field_at(
            -1,
            name=f'Probability to lose is {self._get_lose_probability()}%  ',
            value=f'{self.current_player.mention}, your turn',
            inline=False,
        )
        # TODO: Remove after done testing
        self.game_embed.set_footer(
            text=f'Timeout: {self.timeout} sec'
            f'\n\nTESTING:\nBullet location is {self.bullet_location}\nCurrent chamber is {self.current_chamber}'
        )

    def _set_embed_endgame(self) -> None:
        """Updates embed for game ending scenario."""

        self.game_embed.title = 'RIP'
        self.game_embed.colour = discord.Color.dark_red()
        self.game_embed.set_thumbnail(url=f'{self.current_player.avatar.url}')
        self.game_embed.set_field_at(
            -1,
            name=f'Winner of this round',
            value=f'{self.current_player.mention}',
            inline=False,
        )
        self.game_embed.set_footer(text=f'Score: {self.rounds_played * self.BULLETS_LOADED}')

    def _set_embed_aborted(self) -> None:
        """Updates embed for game aborted scenario."""
        self.game_embed.title = 'Game died of old age'
        self.game_embed.colour = discord.Color.dark_red()
        self.game_embed.set_thumbnail(url=f'{self.current_player.avatar.url}')
        self.game_embed.set_field_at(
            -1,
            name=f'Failed to react in time',
            value=f'{self.current_player.mention}',
            inline=False,
        )
        self.game_embed.set_footer(text=f'Timeout: {self.timeout} sec')

    # endregion

    # region game logic
    def get_next_player(self) -> discord.Member:
        """Cycles through the player list and returns next"""

        return self.players[self.rounds_played % len(self.players)]

    def generate_bullet_position(self) -> int:
        """Randomizes bullet position."""

        return random.randint(1, self.CHAMBER_SLOTS)

    def _get_lose_probability(self) -> float:
        """Calculates probability to lose the game on this turn."""

        return round(100 / (self.CHAMBER_SLOTS - self.blank_shots_in_a_row), 1)

    def _next_round(self) -> None:
        """Sets game states for the next round scenario."""

        def get_chamber_position(chamber_pos: int) -> int:
            chamber_pos += 1
            if chamber_pos > self.CHAMBER_SLOTS:
                chamber_pos = 1
            return chamber_pos

        self.blank_shots_in_a_row += 1
        self.current_player = self.get_next_player()
        self.current_chamber = get_chamber_position(self.current_chamber)
        self._set_embed_next_round()

    def _end_game(self) -> None:
        """Disables interaction and updates embed for game ending scenario."""

        for item in self.children:
            item.disabled = True

        self._set_embed_endgame()
        self.stop()

    # endregion

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

        self._set_embed_aborted()
        await self.message.edit(embed=self.game_embed, view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Simple interaction check to make sure turn-based gameplay."""

        if interaction.user.id == self.current_player.id:
            return True
        await interaction.response.send_message(  # noqa
            f'This choice belongs to {self.current_player.mention} now, sorry!', ephemeral=True
        )
        return False

    @discord.ui.button(emoji='\U0001F525', style=discord.ButtonStyle.red, label='Fire')
    async def trigger(self, interaction: discord.Interaction, button: discord.Button) -> None:
        """Pulls the trigger."""

        if self.current_chamber == self.bullet_location:
            self._end_game()
        else:
            self.rounds_played += 1
            self._next_round()
        await interaction.response.edit_message(embed=self.game_embed, view=self)  # noqa

    @discord.ui.button(style=discord.ButtonStyle.grey, label=f'Spin')
    async def roll(self, interaction: discord.Interaction, button: discord.Button) -> None:
        """Spins the chamber to randomize bullet position."""

        self.bullet_location = self.generate_bullet_position()
        self.blank_shots_in_a_row = 0
        self._set_embed_next_round()
        await interaction.response.edit_message(embed=self.game_embed, view=self)  # noqa


class Games(BaseCog):
    """Discord games commands"""

    @commands.hybrid_command()
    async def roulette(
        self,
        ctx: commands.Context,
        players: commands.Greedy[discord.Member] = None,
    ):
        players = players or []
        players.append(ctx.author)

        # Remove duplicates
        players = list(set(players))

        game_view = RussianRouletteView(players=players)
        game_view.message = await ctx.send(embed=game_view.game_embed, view=game_view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Games(bot))

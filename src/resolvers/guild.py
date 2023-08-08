from src.models.guild import Guild as GuildModel
from src.resolvers import Base as BaseResolver


class Guild(BaseResolver):
    model = GuildModel

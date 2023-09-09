from typing import TYPE_CHECKING, Annotated, Optional

import strawberry

from src.models.member import Member as MemberModel

if TYPE_CHECKING:
    from src.api.definitions.guild import GuildNode
    from src.api.definitions.user import UserNode


@strawberry.type
class MemberNode:
    guild_id: float = strawberry.field(
        description=MemberModel.guild_id.__doc__
    )  # Int cannot represent non 32-bit signed integer value: xxxxxxxxxxxxxxxxxx
    user_id: float = strawberry.field(description=MemberModel.user_id.__doc__)
    display_name: Optional[str] = strawberry.field(description=MemberModel.display_name.__doc__)
    active: bool = strawberry.field(description=MemberModel.active.__doc__)
    guild: Annotated['GuildNode', strawberry.lazy('src.api.definitions.guild')]
    user: Annotated['UserNode', strawberry.lazy('src.api.definitions.user')]

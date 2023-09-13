from typing import List, Optional

import strawberry


@strawberry.input
class UserFilter:
    ids: Optional[List[float]] = strawberry.UNSET
    names: Optional[List[str]] = strawberry.UNSET
    global_names: Optional[List[str]] = strawberry.UNSET


@strawberry.input
class GuildFilter:
    ids: Optional[List[float]] = strawberry.UNSET
    names: Optional[List[str]] = strawberry.UNSET
    owner_ids: Optional[List[float]] = strawberry.UNSET


@strawberry.input
class MemberFilter:
    guild_ids: Optional[List[float]] = strawberry.UNSET
    user_ids: Optional[List[float]] = strawberry.UNSET
    display_names: Optional[List[str]] = strawberry.UNSET
    active: Optional[bool] = True

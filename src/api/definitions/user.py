from typing import TYPE_CHECKING, Annotated, Optional

import strawberry

from src.api.connection import Connection, to_connection
from src.models.user import User as UserModel

if TYPE_CHECKING:
    from src.api.definitions.guild import GuildNode
    from src.api.definitions.member import MemberNode


@strawberry.type
class UserNode:
    id: float = strawberry.field(
        description=UserModel.id.__doc__
    )  # Int cannot represent non 32-bit signed integer value: xxxxxxxxxxxxxxxxxx
    name: str = strawberry.field(description=UserModel.name.__doc__)
    global_name: Optional[str] = strawberry.field(description=UserModel.global_name.__doc__)
    avatar_url: Optional[str] = strawberry.field(description=UserModel.avatar_url.__doc__)
    bot: bool = strawberry.field(description=UserModel.bot.__doc__)

    @strawberry.field
    def owner_of(self) -> Connection[Annotated['GuildNode', strawberry.lazy('src.api.definitions.guild')]]:
        return to_connection(node_type='GuildNode', target=self.owner_of)

    @strawberry.field
    def known_as(self) -> Connection[Annotated['MemberNode', strawberry.lazy('src.api.definitions.member')]]:
        return to_connection(node_type='MemberNode', target=self.known_as)


# def encode_user_cursor(id: int) -> str:
#     """
#     Encodes the given user ID into a cursor.
#
#     :param id: The user ID to encode.
#
#     :return: The encoded cursor.
#     """
#     return b64encode(f"user:{id}".encode("ascii")).decode("ascii")
#
#
# def decode_user_cursor(cursor: str) -> int:
#     """
#     Decodes the user ID from the given cursor.
#
#     :param cursor: The cursor to decode.
#
#     :return: The decoded user ID.
#     """
#     cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
#     return int(cursor_data.split(":")[1])

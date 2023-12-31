from typing import Optional

from discord import Member as DiscordMember
from sqlalchemy import select, tuple_, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.member import Member as MemberModel
from src.resolvers.base import Base as BaseResolver
from src.resolvers.user import User as UserResolver


class Member(BaseResolver):
    model = MemberModel

    @classmethod
    def _resolve_filter(cls, field: str):
        filter_map = {
            'pks': tuple_(cls.model.user_id, cls.model.guild_id).in_,
            'guild_ids': cls.model.guild_id.in_,
            'user_ids': cls.model.user_id.in_,
            'display_names': cls.model.display_name.in_,
            'active': cls.model.active.is_,
        }
        return filter_map[field]

    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: int, guild_id: int) -> Optional[MemberModel]:
        stmt = select(cls.model).where(tuple_(cls.model.user_id, cls.model.guild_id) == (user_id, guild_id))
        result = (await session.scalars(stmt)).unique().one_or_none()
        return result

    # region TODO: revisit and refactor
    @classmethod
    async def create(cls, session: AsyncSession, data: dict) -> MemberModel:
        user_data = data.pop('user')
        user_obj, _ = await UserResolver.get_or_create(session, user_data)

        guild_id = data.pop('guild_id')
        member_obj = cls.model(**data)
        member_obj.user_id = user_obj.id
        member_obj.guild_id = guild_id

        session.add(member_obj)
        return member_obj

    @classmethod
    async def get_or_create(cls, session: AsyncSession, data: dict) -> (MemberModel, bool):
        created = False
        if not (db_obj := await cls.get_by_id(session, user_id=data['user_id'], guild_id=data['guild_id'])):
            db_obj = await cls.create(session, data)
            created = True
        return db_obj, created

    @classmethod
    async def update(cls, session: AsyncSession, data: dict) -> MemberModel:
        user_data = data.pop('user')

        user_id, guild_id = user_data['id'], data.pop('guild_id')
        if not (user_id and guild_id):
            raise ValueError(f'PK is not present in data')
        stmt = (
            update(cls.model)
            .where(tuple_(cls.model.user_id, cls.model.guild_id) == (user_id, guild_id))
            .values(**data)
            .returning(cls.model)
        )
        member_obj = (await session.execute(stmt)).unique().one()[0]
        return member_obj

    @classmethod
    async def update_or_create(cls, session: AsyncSession, data: dict) -> MemberModel:
        if await cls.get_by_id(session, user_id=data['user']['id'], guild_id=data['guild_id']):
            db_obj = await cls.update(session, data)
        else:
            db_obj = await cls.create(session, data)
        return db_obj

    @staticmethod
    def from_discord(member: DiscordMember) -> dict:
        return {
            'guild_id': member.guild.id,
            'display_name': member.display_name,
            'user': UserResolver.from_discord(member),
        }

    # endregion

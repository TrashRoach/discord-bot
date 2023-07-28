from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

bigint_pk = Annotated[int, mapped_column(BigInteger, primary_key=True)]

from typing import Generic, Optional, TypeVar, Union, cast

import strawberry

GenericType = TypeVar('GenericType')


@strawberry.type
class Connection(Generic[GenericType]):
    # TODO: page_info
    # page_info: 'PageInfo' = strawberry.field(description='Information to aid in pagination.')
    edges: list['Edge[GenericType]'] = strawberry.field(description='A list of edges in this connection.')


@strawberry.type
class PageInfo:
    has_next_page: bool = strawberry.field(description='When paginating forwards, are there more items?')
    has_previous_page: bool = strawberry.field(description='When paginating backwards, are there more items?')
    start_cursor: Optional[str] = strawberry.field(description='When paginating backwards, the cursor to continue.')
    end_cursor: Optional[str] = strawberry.field(description='When paginating forwards, the cursor to continue.')


@strawberry.type
class Edge(Generic[GenericType]):
    node: GenericType = strawberry.field(description='The item at the end of the edge.')


def to_connection(node_type: Union[strawberry.type, str], relationship_field) -> Connection:
    """Converts SQLAlchemy's many-relationship fields to connection of specified edge nodes.

    Parameters
    -----------
    node_type:
        Strawberry type to form a Connection Edge Nodes from
    relationship_field:
        many-to-one / many-to-many SQLAlchemy model's field

    Returns
    --------
    Connection[node_type]


    Example
    --------
    to_connection(NodeType, model.one_to_many_field) will result in

    oneToManyField {
        edges {
            node {
                __typename  # NodeType
            }
        }
    }
    """

    edges = [
        Edge(
            node=cast(node_type, obj),
        )
        for obj in relationship_field
    ]
    return Connection(edges=edges)

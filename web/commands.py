import click


@click.command()
def insert():
    from web.auth.models import Role
    from web.auth.models import Permission
    from web.extensions import db

    roles = [
        'admin',
        'staff',
        'user',
    ]
    for role in roles:
        db.session.add(Role(name=role))

    entities = [
        {
            'role_id': 1,
            'entity_id': 94268459,
            'entity_name': 'Kim Peek',
        },
        {
            'role_id': 1,
            'entity_id': 411225042,
            'entity_name': 'BJK',
        },
    ]
    for entity in entities:
        permission = Permission(**entity)
        db.session.add(permission)
    db.session.commit()

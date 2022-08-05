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
            'entity_id': 94268459,
            'entity_name': 'Kim Peek',
        },
        {
            'entity_id': 411225042,
            'entity_name': 'BJK',
        },
    ]
    for entity in entities:
        for role_id in range(1, 4):
            permission = Permission(role_id=role_id, **entity)
            db.session.add(permission)
    db.session.commit()

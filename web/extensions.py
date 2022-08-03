from flask import url_for
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

admin = Admin()
db = SQLAlchemy()
migrate = Migrate()


class PublicSiteLink(MenuLink):
    """Menu link leading to public site."""

    def get_url(self):
        return url_for('index.index')


# Add link on the admin menu leading back to main site
admin.add_link(PublicSiteLink(name='Public Site'))

# Remove duplicate "Home" link on admin menu
admin._menu.pop()

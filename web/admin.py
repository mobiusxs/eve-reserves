from flask import flash
from flask import redirect
from flask import url_for
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView

from web.auth.models import Session
from web.auth.models import Role
from web.auth.models import Permission
from web.extensions import db

session = Session()


class SecureAdminIndexView(AdminIndexView):
    def is_visible(self):
        """Remove duplicate 'Admin Home' link from nav"""

        return False

    @expose('/')
    def index(self):
        # from web.auth.models import Session
        # session = Session()
        user = session.get_current_user()
        if not user:
            return redirect(url_for('auth.authorize'))
        if user.has_role('admin'):
            return self.render(self._template)
        flash('You are not an admin')
        return redirect(url_for('public.index'))


class PublicSiteLink(MenuLink):
    """Menu link leading to public site."""

    def get_url(self):
        return url_for('dashboard.index')


class SecuredModelView(ModelView):
    def is_accessible(self):
        # user = Session().get_current_user()
        user = session.get_current_user()
        return user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.index'))


class SessionModelView(SecuredModelView):
    column_list = ('name', 'character_id', 'corporation_id', 'alliance_id', 'created')
    can_create = False
    can_edit = False


class RoleModelView(SecuredModelView):
    column_list = ('name', 'id')
    form_excluded_columns = ('entities',)
    can_create = False
    can_edit = False
    can_delete = False


class PermissionModelView(SecuredModelView):
    page_size = 20
    # column_searchable_list = ['name', 'character_id', 'corporation_id', 'alliance_id']
    column_filters = ['entity_name', 'role']
    # column_editable_list = ['name']
    create_modal = True
    edit_modal = True
    can_export = True
    column_sortable_list = ['entity_name', 'role.name']


admin = Admin(index_view=SecureAdminIndexView(name='Admin Home'))
admin.add_link(PublicSiteLink(name='Public Site'))
admin.add_view(SessionModelView(model=Session, session=db.session, name='Session', category='Auth'))
admin.add_view(RoleModelView(model=Role, session=db.session, name='Role', category='Auth'))
admin.add_view(PermissionModelView(model=Permission, session=db.session, name='Permission', category='Auth'))

class TestSettings:
    def test_env(self, app):
        assert app.config['ENV'] == 'testing'

    def test_testing(self, app):
        assert app.config['TESTING'] is True

    def test_secret_key(self, app):
        assert app.config['SECRET_KEY'] == 'test'

    def test_sqlalchemy_database_uri(self, app):
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'

    def test_sqlalchemy_track_modifications(self, app):
        assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False

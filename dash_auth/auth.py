from abc import ABCMeta, abstractmethod
import flask
from six import iteritems


class Auth(object):
    __metaclass__ = ABCMeta

    def __init__(self, app):
        self.app = app
        self._overwrite_index()
        self._protect_views()

    def _overwrite_index(self):
        original_index = self.app.server.view_functions['index']

        def wrap_index(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_html()

        self.app.server.view_functions['index'] = wrap_index

    def _protect_views(self):
        # TODO - allow users to white list in case they add their own views
        for view_name, view_method in self.app.server.view_functions.iteritems():
            if view_name != 'index':
                self.app.server.view_functions[view_name] = \
                    self.auth_wrapper(view_method)

    @abstractmethod
    def is_authorized(self):
        pass

    @abstractmethod
    def auth_wrapper(self):
        pass

    @abstractmethod
    def login_html(self):
        pass
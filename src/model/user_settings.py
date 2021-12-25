
class UserSettings:
    def __init__(self):
        self._movie_path = None

    @property
    def movie_path(self):
        return  self._movie_path

    @movie_path.setter
    def movie_path(self, value):
        self._movie_path = value

    @movie_path.deleter
    def movie_path(self):
        del self._movie_path

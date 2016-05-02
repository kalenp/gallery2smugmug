from click import testing
import collections

from g2s import app
from g2s import gallery


class StaticGallery(object):
    def __init__(self, albums):
        self._albums = albums

    @property
    def albums(self):
        return self._iter_albums(self._albums, 0)

    def _iter_albums(self, albums, depth):
        for (name, subalbums) in albums.items():
            yield gallery.Album(name, depth)
            for subalbum in self._iter_albums(subalbums, depth+1):
                yield subalbum


def test_list():
    static_gallery = StaticGallery({
        'Vacation': { 'Mexico': {} },
        'Graduation': {}
    })
    cli = app.CLI(static_gallery, None)

    runner = testing.CliRunner()
    result = runner.invoke(cli, ['list'])

    assert result.exit_code == 0
    assert result.output ==  '''Name: Vacation
\tName: Mexico
Name: Graduation
'''

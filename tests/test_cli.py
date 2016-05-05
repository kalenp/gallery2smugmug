from click import testing
import collections

from g2s import app
from g2s import gallery


class StaticGallery(object):
    def __init__(self, albums):
        self._albums = albums

    @property
    def albums(self):
        return {
            album.name: album for (album, depth) in self._albums
        }

    def iter_albums(self):
        return self._albums


def test_list():
    galleries = collections.defaultdict(
        lambda: StaticGallery([
            (gallery.Album('Vacation'), 0),
            (gallery.Album('Mexico',), 1),
            (gallery.Album('Graduation'), 0),
        ])
    )
    cli = app.CLI(galleries, None)

    runner = testing.CliRunner()
    result = runner.invoke(cli, ['list'])

    assert result.exit_code == 0
    assert result.output ==  '''Name: Vacation
\tName: Mexico
Name: Graduation
'''

def test_list_specific_directory():
    galleries = {
        'first': StaticGallery([
            (gallery.Album('First'), 0),
        ]),
        'second': StaticGallery([
            (gallery.Album('Second'), 0),
        ]),
    }

    cli = app.CLI(galleries, None)

    runner = testing.CliRunner()
    result = runner.invoke(cli, ['list', '--gallery-path=second'])

    assert result.exit_code == 0
    assert result.output ==  '''Name: Second
'''


def test_view_gallery_details():
    photos = [object()] * 5
    galleries = {
        '.': StaticGallery([
            (gallery.Album(
                title='Mexico 2016',
                name='mexico',
                description='We went diving in Cancun.  It was great!',
                photos=photos,
            ), 0)
        ]),
    }

    cli = app.CLI(galleries, None)

    runner = testing.CliRunner()
    result = runner.invoke(cli, ['view', 'mexico'])

    assert result.exit_code == 0
    assert result.output == '''Album: Mexico 2016
    Description: We went diving in Cancun.  It was great!
    Short Name: mexico
    Photo Count: 5
'''

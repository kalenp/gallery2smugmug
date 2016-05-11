from click import testing
import collections

from g2s import app
from g2s import gallery


class StaticGallery(object):
    def __init__(self, albums, photos):
        self.albums = albums
        self.photos = photos

    @property
    def album_names(self):
        return self.albums.iterkeys()


def test_list():
    galleries = collections.defaultdict(
        lambda: StaticGallery({
            'Graduation': gallery.Album('Graduation'),
            'Mexico': gallery.Album('Mexico', parent='Vacation'),
            'Vacation': gallery.Album('Vacation'),
        }, {})
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
        'first': StaticGallery({'First': gallery.Album('First')}, {}),
        'second': StaticGallery({'Second': gallery.Album('Second')}, {}),
    }

    cli = app.CLI(galleries, None)

    runner = testing.CliRunner()
    result = runner.invoke(cli, ['list', '--gallery-path=second'])

    assert result.exit_code == 0
    assert result.output ==  '''Name: Second
'''


def test_view_gallery_details():
    albums = {
        'mexico': gallery.Album(
            title='Mexico 2016',
            name='mexico',
            description='We went diving in Cancun.  It was great!',
        )
    }
    photos = { 'mexico': [object()] * 5 }
    galleries = {
        '.': StaticGallery(albums=albums, photos=photos),
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

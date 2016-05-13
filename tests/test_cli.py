from click import testing
import collections

from g2s import app
from g2s import gallery


class StaticGallery(object):
    def __init__(self, albums, photos, subalbums):
        self.albums = albums
        self.photos = photos
        self.subalbums = subalbums

    @property
    def album_names(self):
        return self.albums.iterkeys()


def test_list():
    galleries = collections.defaultdict(
        lambda: StaticGallery(albums={
            'Graduation': gallery.Album('Graduation'),
            'Mexico': gallery.Album('Mexico', parent='Vacation'),
            'Vacation': gallery.Album('Vacation'),
        }, photos={}, subalbums={})
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
        'first': StaticGallery(
            albums={'First': gallery.Album('First')},
            photos={},
            subalbums={}
        ),
        'second': StaticGallery(
            albums={'Second': gallery.Album('Second')},
            photos={},
            subalbums={}
        ),
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
    subalbums = { 'mexico': [] }
    galleries = {
        '.': StaticGallery(albums=albums, photos=photos, subalbums=subalbums),
    }

    cli = app.CLI(galleries, None)

    runner = testing.CliRunner()
    result = runner.invoke(cli, ['view', 'mexico'])

    assert result.exit_code == 0
    assert result.output == '''Album: Mexico 2016
    Description: We went diving in Cancun.  It was great!
    Short Name: mexico
    Photo Count: 5
    SubAlbum Count: 0
'''

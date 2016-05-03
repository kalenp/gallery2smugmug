import os

from g2s import gallery


class StaticGalleryFS(object):
    def __init__(self, albums, photos):
        self._albums = albums
        self._photos = photos

    @property
    def albums(self):
        return self._albums.itervalues()


def test_gallery_builds_tree():
    vacation = gallery.Album('Vacation')
    mexico = gallery.Album('Mexico', parent='Vacation')
    albums = {
        'Mexico': mexico,
        'Vacation': vacation,
    }
    photos = {}
    galleryfs = StaticGalleryFS(albums, photos)

    gal = gallery.Gallery(galleryfs)

    assert list(gal.albums) == [
        (vacation, 0),
        (mexico, 1),
    ]


class TestSerializer(object):
    VACATION = gallery.Album('Vacation')
    MEXICO = gallery.Album('Mexico', parent='Vacation')
    ALBUMS = ['vacation', 'mexico']

    _serialization = {
        'vacation': VACATION,
        'mexico': MEXICO,
        'albumdb': ALBUMS,
    }

    def loads(self, data):
        return self._serialization[data]


def test_galleryfs_load_albums(fs):
    os.mkdir('albums')
    with open('albums/albumdb.dat', 'w+') as albumdb:
        albumdb.write('albumdb')
    os.mkdir('albums/vacation')
    with open('albums/vacation/album.dat', 'w+') as vacation:
        vacation.write('vacation')
    os.mkdir('albums/mexico')
    with open('albums/mexico/album.dat', 'w+') as mexico:
        mexico.write('mexico')

    galleryfs = gallery.GalleryFilesystem(TestSerializer())

    assert galleryfs.albums == [
        TestSerializer.VACATION,
        TestSerializer.MEXICO,
    ]


def test_unserialize_albumdb_dat():
    ALBUM_DB_DAT = '''a:2:{i:0;s:8:"vacation";i:1;s:6:"mexico";}'''
    serializer = gallery.Serializer()

    albums = serializer.loads(ALBUM_DB_DAT)

    assert albums == [
        'vacation',
        'mexico',
    ]


def test_unserialize_album_dat():
    ALBUM_DAT = '''O:5:"Album":1:{s:6:"fields";a:2:{s:4:"name";s:6:"mexico";s:15:"parentAlbumName";s:8:"vacation";}}'''
    serializer = gallery.Serializer()

    album = serializer.loads(ALBUM_DAT)

    assert album.name == 'mexico'
    assert album.parent == 'vacation'


def test_unserialize_album_optional_parent():
    ALBUM_DAT = '''O:5:"Album":1:{s:6:"fields";a:1:{s:4:"name";s:8:"vacation";}}'''
    serializer = gallery.Serializer()

    album = serializer.loads(ALBUM_DAT)

    assert album.name == 'vacation'
    assert album.parent == None


def test_unserialize_album_case_insensitive():
    ALBUM_DAT = '''O:5:"album":1:{s:6:"fields";a:1:{s:4:"name";s:8:"vacation";}}'''
    serializer = gallery.Serializer()

    album = serializer.loads(ALBUM_DAT)

    assert album.name == 'vacation'
    assert album.parent == None


def test_unserialize_album_additional_properties():
    ALBUM_DAT = '''O:5:"album":1:{s:6:"fields";a:3:{s:4:"name";s:8:"vacation";s:5:"title";s:5:"Vacay";s:11:"description";s:6:"See ya";}}'''
    serializer = gallery.Serializer()

    album = serializer.loads(ALBUM_DAT)

    assert album.name == 'vacation'
    assert album.parent == None
    assert album.title == 'Vacay'
    assert album.description == 'See ya'

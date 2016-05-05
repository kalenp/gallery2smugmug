import os

from g2s import gallery


class StaticGalleryFS(object):
    def __init__(self, albums, photos):
        self._albums = albums
        self._photos = photos

    @property
    def albums(self):
        return self._albums.itervalues()

    @property
    def photos(self):
        return self._photos


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

    assert list(gal.iter_albums()) == [
        (vacation, 0),
        (mexico, 1),
    ]


def test_gallery_albums():
    vacation = gallery.Album('Vacation')
    mexico = gallery.Album('Mexico', parent='Vacation')
    albums = {
        'Mexico': mexico,
        'Vacation': vacation,
    }
    photos = {
        'Mexico': object(),
        'Vacation': object(),
    }
    galleryfs = StaticGalleryFS(albums, photos)

    gal = gallery.Gallery(galleryfs)

    assert gal.albums == albums


def test_gallery_albums_contain_photos():
    vacation = gallery.Album('Vacation')
    mexico = gallery.Album('Mexico', parent='Vacation')
    albums = {
        'Mexico': mexico,
        'Vacation': vacation,
    }
    mexico_photos = object()
    vacation_photos = object()
    photos = {
        'Mexico': mexico_photos,
        'Vacation': vacation_photos,
    }
    galleryfs = StaticGalleryFS(albums, photos)

    gal = gallery.Gallery(galleryfs)

    assert {name: album.photos for (name, album) in gal.albums.items()} == photos


class TestSerializer(object):
    ALBUMS = ['vacation', 'mexico']
    MEXICO = object()
    MEXICO_PHOTOS = object()
    VACATION = object()
    VACATION_PHOTOS = object()

    _serialization = {
        'albumdb': ALBUMS,
        'mexico': MEXICO,
        'mexico_photos': MEXICO_PHOTOS,
        'vacation': VACATION,
        'vacation_photos': VACATION_PHOTOS,
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


def test_galleryfs_load_photos(fs):
    os.mkdir('albums')
    with open('albums/albumdb.dat', 'w+') as albumdb:
        albumdb.write('albumdb')
    os.mkdir('albums/vacation')
    with open('albums/vacation/photos.dat', 'w+') as vacation:
        vacation.write('vacation_photos')
    os.mkdir('albums/mexico')
    with open('albums/mexico/photos.dat', 'w+') as mexico:
        mexico.write('mexico_photos')

    galleryfs = gallery.GalleryFilesystem(TestSerializer())

    assert galleryfs.photos == {
        'vacation': TestSerializer.VACATION_PHOTOS,
        'mexico': TestSerializer.MEXICO_PHOTOS,
    }


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


PHOTOS_DAT = '''a:1:{i:0;O:9:"AlbumItem":19:{s:8:"exifData";N;s:4:"rank";N;s:11:"extraFields";a:0:{}s:14:"highlightImage";N;s:5:"image";O:5:"Image":12:{s:7:"thumb_x";N;s:7:"thumb_y";N;s:4:"name";s:10:"Untitled_4";s:11:"thumb_width";N;s:10:"raw_height";i:1200;s:12:"thumb_height";N;s:6:"height";i:436;s:5:"width";i:640;s:7:"version";i:31;s:9:"raw_width";i:1760;s:4:"type";s:3:"jpg";s:11:"resizedName";s:16:"Untitled_4.sized";}s:7:"emailMe";N;s:5:"owner";s:21:"1069957692_2062256631";s:8:"comments";N;s:6:"clicks";i:68;s:7:"caption";s:24:"The view from our hotel.";s:7:"version";i:31;s:10:"uploadDate";i:1079529094;s:11:"isAlbumName";N;s:8:"keywords";N;s:9:"highlight";b:0;s:6:"hidden";N;s:7:"preview";N;s:9:"thumbnail";O:5:"Image":12:{s:7:"thumb_x";N;s:7:"thumb_y";N;s:4:"name";s:16:"Untitled_4.thumb";s:11:"thumb_width";N;s:10:"raw_height";i:102;s:12:"thumb_height";N;s:6:"height";i:102;s:5:"width";i:150;s:7:"version";i:31;s:9:"raw_width";i:150;s:4:"type";s:3:"jpg";s:11:"resizedName";N;}s:15:"itemCaptureDate";a:11:{i:0;i:1079529094;s:4:"mday";i:17;s:7:"seconds";i:34;s:5:"month";s:5:"March";s:5:"hours";s:2:"05";s:3:"mon";s:2:"03";s:4:"year";i:2004;s:4:"yday";i:76;s:4:"wday";i:3;s:7:"minutes";i:11;s:7:"weekday";s:9:"Wednesday";}}}'''


def test_unserialize_photos():
    serializer = gallery.Serializer()

    photos = serializer.loads(PHOTOS_DAT)

    assert len(photos) == 1
    assert photos[0].image.type == 'jpg'

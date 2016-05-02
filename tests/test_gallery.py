from g2s import gallery


def test_parse_albums():
    ALBUM_DB_DAT = '''a:2:{i:0;s:8:"Vacation";i:1;s:6:"Mexico";}'''
    albums = gallery.parse_albumsdb(ALBUM_DB_DAT)

    assert albums == [
        "Vacation",
        "Mexico",
    ]


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

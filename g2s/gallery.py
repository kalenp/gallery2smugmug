import phpserialize

from . import util

class Gallery(object):
    def __init__(self, galleryfs):
        self._galleryfs = galleryfs

    @property
    def albums(self):
        albums = {}
        photos_dict = self._galleryfs.photos
        for album in self._galleryfs.albums:
            name = album.name
            album.photos = photos_dict[name]
            albums[name] = album
        return albums

    def iter_albums(self):
        return self.album_tree.iter_objects(0)

    @property
    def album_tree(self):
        tree = util.ParentNameTree()
        for album in self._galleryfs.albums:
            tree.add_object(album)
        return tree


class Album(object):
    def __init__(self, name, parent=None, title=None, description=None,
                 photos=[]):
        self.name = name
        self.description = description
        self.parent = parent
        self.title = title
        self.photos = photos

    @classmethod
    def from_fields(cls, fields):
        kwargs = {
            key: value for (key, value) in fields.iteritems()
            if key in ['name', 'title', 'description']
        }
        if 'parentAlbumName' in fields:
            kwargs['parent'] = fields['parentAlbumName']
        return cls(**kwargs)


class GalleryFilesystem(object):
    def __init__(self, serializer):
        self._serializer = serializer

    @property
    def albums(self):
        albums = []
        for name in self._album_names:
            with open('albums/{}/album.dat'.format(name), 'r') as album_dat:
                albums.append(self._serializer.loads(album_dat.read()))
        return albums

    @property
    def photos(self):
        photos = {}
        for name in self._album_names:
            with open('albums/{}/photos.dat'.format(name), 'r') as photos_dat:
                photos[name] = self._serializer.loads(photos_dat.read())
        return photos

    @property
    def _album_names(self):
        with open('albums/albumdb.dat', 'r') as albumdb_dat:
            albumdb = self._serializer.loads(albumdb_dat.read())
        return albumdb


class Serializer(object):
    def loads(self, data):
        def object_hook(name, d):
            name = name.lower()
            if name == 'album':
                fields = d['fields']
                return Album.from_fields(fields)
            else:
                return phpserialize.phpobject(name, d)

        loaded = phpserialize.loads(data, object_hook=object_hook)
        if isinstance(loaded, dict):
            loaded = phpserialize.dict_to_list(loaded)
        return loaded

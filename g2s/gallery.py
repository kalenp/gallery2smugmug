import datetime

import phpserialize

from . import util


class Album(object):
    def __init__(self, name, parent=None, title=None, description=None):
        self.name = name
        self.description = description
        self.parent = parent
        self.title = title


class Photo(object):
    def __init__(self, name, image_type=None, caption=None, captured_at=None):
        self.name = name
        self.image_type = image_type
        self.caption = caption
        self.captured_at = captured_at


class AlbumItem(object):
    PHOTO = 'photo'
    SUBALBUM = 'subalbum'

    @classmethod
    def SubAlbum(cls, name, **kwargs):
        return cls(name, cls.SUBALBUM, **kwargs)

    @classmethod
    def Photo(cls, name, **kwargs):
        return cls(name, cls.PHOTO, **kwargs)

    def __init__(self, name, obj_type, image_type=None, caption=None,
                 captured_at=None):
        self.name = name
        self.obj_type = obj_type
        self.image_type = image_type
        self.caption = caption
        self.captured_at = captured_at


class Serializer(object):
    def loads(self, data):
        def object_hook(name, d):
            # Need to lowercase these, because the data is inconsistent in how
            # it names the classes
            name = name.lower()
            if name == 'album':
                fields = d['fields']
                return Album(name=fields['name'], title=fields.get('title'),
                             description=fields.get('description'),
                             parent=fields.get('parentAlbumName'))
            elif name == 'albumitem':
                # This contains info about the image and the thumbnail.  But
                # since we don't care about the thumbnail, just collapse this
                # together with the contained image, which we already parsed
                kwargs = {'caption': d['caption']}
                if d['isAlbumName']:
                    return AlbumItem.SubAlbum(d['isAlbumName'],
                                              caption=d['caption'])
                else:
                    image = d['image']
                    captured_at=datetime.date.fromtimestamp(
                        d['itemCaptureDate'][0])
                    return AlbumItem.Photo(image.name,
                                           caption=d['caption'],
                                           image_type=image.image_type,
                                           captured_at=captured_at)
            elif name == 'image':
                return Photo(name=d['name'], image_type=d['type'])

        loaded = phpserialize.loads(data, object_hook=object_hook)
        if isinstance(loaded, dict):
            loaded = phpserialize.dict_to_list(loaded)
        return loaded


class GalleryFilesystem(object):
    def __init__(self, directory='.', serializer=Serializer()):
        self._directory = directory
        self._serializer = serializer
        self._album_names = None

    @property
    def _album_dir(self):
        return '{}/albums'.format(self._directory)

    @property
    def album_names(self):
        '''Get a list of all of the album names'''

        if self._album_names is None:
            albumdb_dat_path = '{}/albumdb.dat'.format(self._album_dir)
            with open(albumdb_dat_path, 'r') as albumdb_dat:
                albumdb = self._serializer.loads(albumdb_dat.read())
            self._album_names = albumdb
        return self._album_names

    @property
    def albums(self):
        '''Get a mapping of album names to deserialized album objects

        The mapping uses a lazy loader, so not all of the keys are present
        initially, but this also reduces the initialization overhead.  Use
        `album_names` to get the list of available albums.
        '''

        def load_album(name):
            album_dat_path = '{}/{}/album.dat'.format(self._album_dir, name)
            with open(album_dat_path, 'r') as album_dat:
                return self._serializer.loads(album_dat.read())
        return util.LazyLoadingDict(load_album)

    @property
    def photos(self):
        '''Get a mapping of album names to deserialized photos objects

        The mapping uses a lazy loader, so not all of the keys are present
        initially, but this also reduces the initialization overhead.  Use
        `album_names` to get the list of available albums.
        '''

        def load_photos(name):
            photos_dat_path = '{}/{}/photos.dat'.format(self._album_dir, name)
            with open(photos_dat_path, 'r') as photos_dat:
                return self._serializer.loads(photos_dat.read())
        return util.LazyLoadingDict(load_photos)

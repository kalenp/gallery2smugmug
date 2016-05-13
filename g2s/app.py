import click

from . import util

gallery_path_option = click.option('--gallery-path', default='.')

def CLI(galleries, smugmug):

    @click.group()
    def cli():
        pass

    @cli.command()
    @gallery_path_option
    def list(gallery_path):
        gallery = galleries[gallery_path]
        tree = util.ParentNameTree(gallery.albums[album_name]
                                   for album_name in gallery.album_names)
        for (album, depth) in tree.iter_objects():
            click.echo('{}Name: {}'.format('\t'*depth, album.name))

    @cli.command()
    @click.argument('album_name')
    @gallery_path_option
    def view(album_name, gallery_path):
        gallery = galleries[gallery_path]
        album = gallery.albums[album_name]
        photos = gallery.photos[album_name]
        subalbums = gallery.subalbums[album_name]
        album_format = \
'''Album: {}
    Description: {}
    Short Name: {}
    Photo Count: {}
    SubAlbum Count: {}'''
        click.echo(album_format.format(
            album.title, album.description, album.name, len(photos),
            len(subalbums)
        ))

    return cli

import click

gallery_path_option = click.option('--gallery-path', default='.')

def CLI(galleries, smugmug):

    @click.group()
    def cli():
        pass

    @cli.command()
    @gallery_path_option
    def list(gallery_path):
        for (album, depth) in galleries[gallery_path].iter_albums():
            click.echo('{}Name: {}'.format('\t'*depth, album.name))

    @cli.command()
    @click.argument('album_name')
    @gallery_path_option
    def view(album_name, gallery_path):
        album = galleries[gallery_path].albums[album_name]
        album_format = \
'''Album: {}
    Description: {}
    Short Name: {}
    Photo Count: {}'''
        click.echo(album_format.format(
            album.title, album.description, album.name, len(album.photos)
        ))

    return cli

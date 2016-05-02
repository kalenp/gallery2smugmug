import click

def CLI(gallery, smugmug):

    @click.group()
    def cli():
        pass

    @cli.command()
    def list():
        for album in gallery.albums:
            click.echo('{}Name: {}'.format('\t'*album.depth, album.title))

    return cli

import click

def CLI(galleries, smugmug):

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.option('--gallery-path', default='.')
    def list(gallery_path):
        for (album, depth) in galleries[gallery_path].albums:
            click.echo('{}Name: {}'.format('\t'*depth, album.name))

    return cli

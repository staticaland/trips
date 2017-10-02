# -*- coding: utf-8 -*-

"""Console script for Trips."""

import click

from trips import oslo


@click.command()
@click.argument('from_place')
@click.argument('to_place')
def main(from_place, to_place):
    """Console script for ruter_cli."""

    click.echo('Trying to show trip')

    oslo.trip(from_place, to_place)


if __name__ == "__main__":
    main()

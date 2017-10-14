# -*- coding: utf-8 -*-

import click

from trips import oslo


@click.command()
@click.argument('from_place')
@click.argument('to_place')
def main(from_place, to_place):

    proposals = oslo.proposals(from_place, to_place)

    oslo.print_proposals(proposals)


if __name__ == "__main__":
    main()

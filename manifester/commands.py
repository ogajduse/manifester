"""Defines the CLI commands for Manifester."""
import click

from logzero import logger
from manifester import Manifester, helpers
from manifester.settings import settings
from pathlib import Path


# To do: add a command for returning subscription pools
@click.group
def cli():
    """Command-line interface for manifester."""
    pass


@cli.command()
@click.option(
    "--manifest_category",
    type=str,
    help="Category of manifest (golden_ticket or robottelo_automation by default)",
)
@click.option("--allocation_name", type=str, help="Name of upstream subscription allocation")
def get_manifest(manifest_category, allocation_name):
    """Return a subscription manifester based on the settings for the provided manifest_category."""
    manifester = Manifester(manifest_category, allocation_name)
    manifester.create_subscription_allocation()
    for sub in manifester.subscription_data:
        manifester.process_subscription_pools(
            subscription_pools=manifester.subscription_pools,
            subscription_data=sub,
        )
    manifester.trigger_manifest_export()

@cli.command()
@click.option('--details', is_flag=True, help='Display full inventory details')
def inventory(details):
  logger.info("Displaying local inventory data")
  click.echo(helpers.load_inventory_file(Path(settings.inventory_path)))

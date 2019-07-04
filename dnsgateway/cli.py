# Copyright (c) 2019 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""dnsgateway.cli module."""

import logging

import click

from dnsgateway.client import (DnsGatewayClient,
                               DEVELOPMENT_ENDPOINT, PRODUCTION_ENDPOINT)

log = logging.getLogger(__name__)


def loglevel(verbosity=0):
    """Set logging verbosity."""
    level = 40 - (verbosity * 10)
    logging.basicConfig(level=level)
    return


@click.group()
@click.option("-u", "--username", envvar="DNS_GATEWAY_USERNAME",
              help="Username for API authentication")
@click.option("-p", "--password", envvar="DNS_GATEWAY_PASSWORD",
              help="Password for API authentication")
@click.option("--endpoint-url", help="API endpoint URL")
@click.option("--pro", "endpoint_url", flag_value=PRODUCTION_ENDPOINT,
              help=f"Shorthand for '--endpoint-url={PRODUCTION_ENDPOINT}'",
              default=True)
@click.option("--dev", "endpoint_url", flag_value=DEVELOPMENT_ENDPOINT,
              help=f"Shorthand for '--endpoint-url={DEVELOPMENT_ENDPOINT}'")
@click.option("-v", "verbosity", count=True, help="Increase logging verbosity")
@click.version_option()
@click.pass_context
def main(ctx, username, password, endpoint_url, verbosity):
    """Manage domain registrations via the DNS Gateway API.

    See https://postman.gateway.africa/ for details.
    """
    loglevel(verbosity=verbosity)
    log.debug("Setting up client instance")
    ctx.obj = DnsGatewayClient(endpoint=endpoint_url,
                               username=username, password=password)


@main.group(help="Manage domains")
@click.pass_context
def domain(ctx):
    """Domain management command group."""
    pass


@domain.command(name="list", help="List domains")
@click.pass_context
def list_domains(ctx):
    """List registered domains."""
    log.debug("Listing domains")
    try:
        for domain in ctx.obj.domains:
            click.echo(domain)
    except Exception:
        raise click.Abort


@domain.command(name="show", help="Show domain details")
@click.argument("domain_name")
@click.pass_context
def show_domain(ctx, domain_name):
    """Show domain details."""
    log.debug(f"Getting details for domain '{domain_name}'")
    try:
        domain = ctx.obj.domain(name=domain_name)
        click.echo(domain)
    except Exception:
        raise click.Abort


@main.group(help="Manage contacts")
@click.pass_context
def contact(ctx):
    """Contact management command group."""
    pass


@contact.command(name="list", help="List contacts")
@click.pass_context
def list_contacts(ctx):
    """List registered contacts."""
    log.debug("Listing contacts")
    try:
        for contact in ctx.obj.contacts:
            click.echo(contact)
    except Exception:
        raise click.Abort


@contact.command(name="show", help="Show contact details")
@click.argument("contact_id")
@click.pass_context
def show_contact(ctx, contact_id):
    """Show contact details."""
    log.debug(f"Getting details for contact '{contact_id}'")
    try:
        contact = ctx.obj.contact(id=contact_id)
        click.echo(contact)
    except Exception:
        raise click.Abort


@main.group(help="Manage zones")
@click.pass_context
def zone(ctx):
    """Zone management command group."""
    pass


@zone.command(name="list", help="List zones")
@click.pass_context
def list_zones(ctx):
    """List available zones."""
    log.debug("Listing zones")
    try:
        for zone in ctx.obj.zones:
            click.echo(zone)
    except Exception:
        raise click.Abort

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

from dnsgateway.client import (DEVELOPMENT_ENDPOINT,
                               DnsGatewayClient,
                               PRODUCTION_ENDPOINT)

log = logging.getLogger(__name__)


def loglevel(verbosity=0):
    """Set logging verbosity."""
    level = 40 - (verbosity * 10)
    logging.basicConfig(level=level)
    return


@click.group()
@click.option("-u", "--username",
              envvar="DNS_GATEWAY_USERNAME", show_envvar=True,
              help="Username for API authentication")
@click.option("-p", "--password",
              envvar="DNS_GATEWAY_PASSWORD", show_envvar=True,
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
    except Exception as e:
        log.error(e)
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
    except Exception as e:
        log.error(e)
        raise click.Abort


@domain.command(name="check", help="Check domain name availability")
@click.argument("domain_name")
@click.option("--operation", default="create", help="Domain operation",
              type=click.Choice(("transfer", "create", "renew", "restore")))
@click.pass_context
def check_domain(ctx, domain_name, operation):
    """Check domain availability."""
    log.debug(f"Checking availability of domain {domain_name}")
    try:
        charge = ctx.obj.check_domain(name=domain_name, op=operation)
        click.echo(charge)
    except Exception as e:
        log.error(e)
        raise click.Abort


@domain.command(name="create", help="Create new domain")
@click.option("--name", required=True, help="Domain name")
@click.option("--period", default=1, help="Registration period in years")
@click.option("--autorenew", is_flag=True, help="Enable autorenewal")
@click.option("--host", "-h", "hosts", multiple=True, help="Nameserver host")
@click.option("--admin", required=True, help="Administrative contact id")
@click.option("--registrant", required=True, help="Registrant contact id")
@click.option("--billing", required=True, help="Billing contact id")
@click.option("--tech", required=True, help="Technical contact id")
@click.option("--accept-charge", "-y", "accept", is_flag=True,
              help="Accept registration charge without prompting")
@click.pass_context
def create_domain(ctx, **kwargs):
    """Create a new domain."""
    log.debug(f"Checking availability of domain {kwargs['name']}")
    try:
        charge = ctx.obj.check_domain(name=kwargs["name"], op="create")
    except Exception as e:
        log.error(e)
        raise click.Abort
    if charge is False:
        err = RuntimeError(f"Domain {kwargs['name']} is not available")
        log.error(err)
        raise click.Abort
    accept = kwargs.pop("accept")
    if not accept:
        click.confirm(f"Accept registration charge of ${charge} "
                      f"for {kwargs['name']}?", abort=True)
    log.debug("Creating new domain")
    log.debug(kwargs)
    try:
        domain = ctx.obj.create_domain(**kwargs, charge=charge)
        click.echo(domain)
    except Exception as e:
        log.error(e)
        raise click.Abort


@domain.command(name="delete", help="Delete domain")
@click.argument("domain_name")
@click.pass_context
def delete_domain(ctx, domain_name):
    """Delete domain."""
    log.debug(f"Deleting domain '{domain_name}'")
    try:
        domain = ctx.obj.domain(name=domain_name)
        domain.delete()
        click.echo(f"Domain {domain_name} deleted")
    except Exception as e:
        log.error(e)
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
    except Exception as e:
        log.error(e)
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
    except Exception as e:
        log.error(e)
        raise click.Abort


@contact.command(name="create", help="Create new contact")
@click.option("--id", required=True, help="Contact ID")
@click.option("--name", required=True, help="Contact name")
@click.option("--org", help="Contact organisation")
@click.option("--email", required=True, help="Contact email address")
@click.option("--phone", required=True, help="Contact phone number")
@click.option("--fax", help="Contact fax number")
@click.option("--address1", help="Contact address line 1")
@click.option("--address2", help="Contact address line 2")
@click.option("--address3", help="Contact address line 3")
@click.option("--city", required=True, help="Contact address city")
@click.option("--province", help="Contact address province")
@click.option("--code", help="Contact address postal code")
@click.option("--country", required=True, help="Contact address country code")
@click.pass_context
def create_contact(ctx, **kwargs):
    """Create a new contact."""
    log.debug("Creating new contact")
    log.debug(kwargs)
    try:
        contact = ctx.obj.create_contact(**kwargs)
        click.echo(contact)
    except Exception as e:
        log.error(e)
        raise click.Abort


@contact.command(name="delete", help="Delete contact")
@click.argument("contact_id")
@click.pass_context
def delete_contact(ctx, contact_id):
    """Delete contact."""
    log.debug(f"Deleting contact '{contact_id}'")
    try:
        contact = ctx.obj.contact(id=contact_id)
        contact.delete()
        click.echo(f"Contact {contact_id} deleted")
    except Exception as e:
        log.error(e)
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
    except Exception as e:
        log.error(e)
        raise click.Abort

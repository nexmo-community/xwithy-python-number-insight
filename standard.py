import os
import click
from terminaltables import SingleTable
import nexmo


@click.command()
@click.argument('number')
def standard_insight(number):

    # Clear the terminal
    click.clear()

    client = nexmo.Client(
        key=os.environ['NEXMO_API_KEY'],
        secret=os.environ['NEXMO_API_SECRET']
    )

    response = client.get_standard_number_insight({'number': number})

    if response['status'] == 0:

        # Number format table
        number_data = [
            [
                click.style('International format', bold=True),
                click.style(response['international_format_number'], fg='green')
            ],
            [
                click.style('National format', bold=True),
                click.style(response['national_format_number'], fg='green')
            ]
        ]

        number_table = SingleTable(number_data)
        number_table.inner_heading_row_border = False
        number_table.outer_border = False

        # Country code information table
        country_data = [[
            click.style('Key', bold=True, fg='green'),
            click.style('Value from Nexmo', bold=True, fg='green')
        ]]

        for k in ['country_name', 'country_prefix', 'country_code', 'country_code_iso3']:
            country_data.append([
                k.replace('_', ' '),
                response[k]
            ])

        country_table = SingleTable(country_data)
        country_table.title = 'COUNTRY INFORMATION'

        # Carrier table
        carrier_data = [[
            click.style('Key', bold=True, fg='green'),
            click.style('Value from Nexmo', bold=True, fg='green')
        ]]

        for key, value in response['current_carrier'].items():
            carrier_data.append([
                key.replace('_', ' '),
                value
            ])

        carrier_table = SingleTable(carrier_data)
        carrier_table.title = 'CURRENT CARRIER'

        click.echo(" ")
        click.echo(number_table.table)
        click.echo(" ")
        click.echo(country_table.table)
        click.echo(" ")
        click.echo(carrier_table.table)

    else:
        # There's been some sort of error, print the message from Nexmo
        click.secho(
            response['status_message'],
            bold=True,
            bg='red',
            fg='white'
        )


if __name__ == '__main__':
    standard_insight()

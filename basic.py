import os
import click
from terminaltables import SingleTable
import nexmo


@click.command()
@click.argument('number')
def basic_insight(number):

    # Clear the terminal
    click.clear()

    client = nexmo.Client(
        key=os.environ['NEXMO_API_KEY'],
        secret=os.environ['NEXMO_API_SECRET']
    )

    response = client.get_basic_number_insight({'number': number})

    if response['status'] == 0:
        data = []

        # First row is table header
        data.append([
            click.style('Key', bold=True, fg='green'),
            click.style('Value from Nexmo', bold=True, fg='green')
        ])

        for key, value in response.items():
            data.append([
                key.replace("_", " "),
                value
            ])

        table = SingleTable(data)
        table.title = click.style('BASIC')
        click.echo(table.table)

    else:
        # There's been some sort of error, print the message from Nexmo
        click.secho(
            response['status_message'],
            bold=True,
            bg='red',
            fg='white'
        )


if __name__ == '__main__':
    basic_insight()

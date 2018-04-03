import os
import click
from fabulous import utils, image
import nexmo


@click.command()
@click.argument('number')
@click.argument('ip')
def advanced_insight(number, ip):

    # Clear the terminal
    click.clear()

    client = nexmo.Client(
        key=os.environ['NEXMO_API_KEY'],
        secret=os.environ['NEXMO_API_SECRET']
    )

    response = client.get_advanced_number_insight({
        'number': number,
        'ip': ip
    })

    if response['status'] == 0:
        click.echo(" ")
        if response['ip']['ip_match_level'] == 'country':
            click.echo(image.Image("yes.png"))
        else:
            click.echo(image.Image("no.png"))

    else:
        # There's been some sort of error, print the message from Nexmo
        click.secho(
            response['status_message'],
            bold=True,
            bg='red',
            fg='white'
        )


if __name__ == '__main__':
    advanced_insight()

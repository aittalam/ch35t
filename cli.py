import click
import click_repl
from ch35t import Chest
import os
from prompt_toolkit.history import FileHistory


def custom_help(ctx, sections=['usage', 'short_help_str', 'options', 'commands'], return_dict=False):
    """ 
        Return only a part of the sections the default help is split into

        click's help is great, but it assumes every command is always ran
        directly from the command line. Being in a CLI, the default help
        is a bit misleading.

        This method allows one to choose which sections of the default help
        are shown, so e.g. one can skip "usage" which is thought for the CLI.

        Using this help is still a bit cumbersome as it requires to disable
        the default one and explicitly call this method, so I am actually
        not sure if/how much I am going to use it... Hey, this is what you
        get for trying some highly-under-development code :-)
    """

    help_str = ctx.get_help()
    help_dict = {}
    help_sections = ['usage', 'short_help_str', 'options', 'commands']
    idx = 0

    # clean sections from commands if not group:
    if type(ctx.command) != click.core.Group and 'commands' in sections:
        sections.remove('commands')

    # init dict
    for k in help_sections:
        help_dict[k] = ""

    # parse help and split it in different sections
    for line in help_str.split("\n"):
        if idx == 0:
            script_name = " "+__file__.split("/")[-1]
            # remove script name from usage
            line = line.replace(script_name,"")
        if line == "":
            idx += 1
            continue
        else:
            help_dict[help_sections[idx]] += f"{line}\n"

    if return_dict:
        return(help_dict)

    help_out = ""
    for section in sections:
        help_out += help_dict[section] + "\n"
    
    return(help_out)
    

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """CLI-based ch35t manipulation tool"""

    # initialize the obj (a dict) that will hold our chest
    # (and possibly other metadata we want to persist inside the REPL)
    ctx.ensure_object(dict)

    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


@cli.command()
@click.pass_context
def status(ctx):
    """Shows the current status"""
    
    click.secho("You look around you and you see...", bold=True)

    chest = ctx.obj.get("chest")
    if chest is None:
        click.echo("🤷 no chest is around, go get one!")
    else:
        click.echo("📦 you have a chest with you")
        click.echo(f" - the chest has a label on it, saying its name is ", nl=False)
        click.secho(chest.name(), bold=True)
        if chest.author() is not None:
            click.echo(f" - there is also a name on the label, it appears the chest creator is ", nl=False)
            click.secho(chest.author(), bold=True)
        else:
            click.echo(f" - the creator of this chest is unknown")

    click.echo()


@cli.command()
@click.pass_context
@click.option('--json', help="Chest JSON (string, file:// or http(s)://)")
def get(ctx, json):
    """Gets a chest (JSON string, file, or URL)"""

    if json is None:
        # keep init with null JSON disabled until we have all the
        # methods for manual loading exposed
        click.secho("You should provide a chest in JSON format", fg='yellow')
    else:
        try:
            ctx.obj["chest"] = Chest(json, chests_dir="./chests")
            click.secho("📦 I got a chest! Now check if it is a valid one", fg='green')
        except Exception as e:
            click.secho(f"[x] {e}", fg='red')


@cli.command()
@click.pass_context
@click.option('--dump', help="Just show the raw hint object", is_flag=True, default=False, show_default=True)
def hint(ctx, dump):
    """Shows a chest's hint"""
    chest = ctx.obj.get("chest")
    if chest is None:
        click.secho("It appears you have no chest, try to get one first", fg='yellow')
    else:
        if dump:
            click.echo(chest.hint.dump())
        else:
            click.secho("Here is the hint to open your chest:", bold=True)
            click.echo(chest.hint)


@cli.command()
@click.pass_context
@click.option('--dump', help="Just show the raw payload object", is_flag=True, default=False, show_default=True)
def payload(ctx, dump):
    """Shows a chest's payload"""
    chest = ctx.obj.get("chest")
    if chest is None:
        click.secho("It appears you have no chest, try to get one first", fg='yellow')
    else:
        if dump:
            click.echo(chest.payload.dump())
        else:
            click.secho("Here is the content of your chest:", bold=True)
            click.echo(chest.payload)


@cli.command()
@click.pass_context
@click.option('--dump', help="Just show the raw hint object", is_flag=True, default=False, show_default=True)
def label(ctx, dump):
    """Shows a chest's label"""
    chest = ctx.obj.get("chest")
    if chest is None:
        click.secho("It appears you have no chest, try to get one first", fg='yellow')
    else:
        if dump:
            click.echo(chest.label.dump())
        else:
            click.secho("You look at the label attached to the chest and read the following:", bold=True)
            click.echo("-------------------------------------------------------------------")
            click.echo("The name of this chest is: ", nl=False)
            click.secho(chest.name(), bold=True)
            click.echo("The name of its creator is: ", nl=False)
            author = "Unknown" if chest.author() is None else chest.author()
            click.secho(author, bold=True)


@cli.command(add_help_option=False)
@click.pass_context
def help(ctx):
    """Well you are here, so I suppose you know already ;-)"""
    # get custom help dictionary  
    help_dict = custom_help(ctx.parent, return_dict=True)

    click.echo()
    click.secho(help_dict['short_help_str'], bold=True, nl=False)
    click.echo("------------------------------------------\n")
    click.echo(help_dict['commands'])
    click.echo("Type \"COMMAND --help\" to get help about a command\n")


@cli.command()
@click.pass_context
def validate(ctx):
    """Validate the chest JSON according to Ch35t schema"""
    chest = ctx.obj.get("chest")
    if chest is None:
        click.secho("It appears you have no chest, try to get one first", fg='yellow')
    else:
        try:
            chest.validate()
            click.secho("This chest is valid!", fg='green')
        except Exception as e:
            click.secho("Oh no, there seems to be a validation error:", fg='red')
            print(e)


@cli.command()
@click.pass_context
@click.option("--key", prompt="Enter the key to open the chest", help="The key to be used to open the chest")
def unlock(ctx, key):
    """Unlock a chest provided a key"""
    chest = ctx.obj.get("chest")
    if chest is None:
        click.secho("It appears you have no chest, try to get one first", fg='yellow')
    else:
        if chest.unlock(key):
            click.secho("The chest is now unlocked!", fg='green')
        else:
            click.secho("The key is not the right one, the chest is still locked", fg='red')


def repl():
    """Start an interactive session"""
    prompt_kwargs = {
        'history': FileHistory(os.path.expanduser('~/.repl_history'))
    }
    click_repl.repl(click.get_current_context(), prompt_kwargs=prompt_kwargs)


if __name__ == '__main__':
    cli(obj={})


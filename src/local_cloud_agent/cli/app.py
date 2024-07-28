import typer
from common import constants
from importlib import metadata


app = typer.Typer(name=constants.lower_keyword, no_args_is_help=True)

sub_app = typer.Typer(no_args_is_help=True)
app.add_typer(sub_app)

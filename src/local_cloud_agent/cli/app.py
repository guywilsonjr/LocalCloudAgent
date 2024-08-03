import typer
from local_cloud_agent.common import constants


app = typer.Typer(name=constants.lower_keyword, no_args_is_help=True)

sub_app = typer.Typer(no_args_is_help=True)
app.add_typer(sub_app)

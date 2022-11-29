import click
from app.domain.commands.computation import Solver


@click.group(help="CLI pour l'outil d'équilibrage d'un réseau de gaz.")
def main():
    pass


@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(),
    required=True,
    prompt="Spécifiez le fichier de configuration à utiliser.",
    help="Fichier de configuration de calcul",
)
@click.option(
    "--input",
    "-i",
    type=click.Path(),
    required=True,
    prompt="Spécifiez le fichier d'entrée.",
    help="Fichier de définition du réseau",
)
@click.option(
    "--bio",
    is_flag=True,
    show_default=True,
    default=False,
    help="Calcul des proportions de gaz bio.",
)
def run(config, input, bio):
    # TODO : Mettre ici en forme les données pour le passer au solver
    #
    # Initialisation de la commande
    s = Solver(config)
    # Lancement de la commande
    s.run()


main.add_command(run)

if __name__ == "__main__":
    exit(main())

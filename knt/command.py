#!/usr/bin/env python

from collections import defaultdict
import os
from subprocess import run
import tempfile
import textwrap

import click
from pygments import highlight
from pygments.lexers import YamlLexer
from pygments.formatters import TerminalTrueColorFormatter
import requests
from tabulate import tabulate
import yaml


class TemplateRepository(object):
    """
    Pass-through data structure for using short names to reference known templates
    """

    def __init__(self):
        url_template = "https://raw.githubusercontent.com/knative/build-templates/master/{dir}/{file}.yaml"
        templates = {}
        for template in ["buildah", "kaniko", "buildpack", "bazel"]:
            templates[template] = url_template.format(dir=template, file=template)

        for builder in ["maven", "gradle"]:
            templates["jib-{}".format(builder)] = url_template.format(
                dir="jib", file="jib-{}".format(builder)
            )

        templates["buildkit"] = url_template.format(
            dir="buildkit", file="1-buildtemplate"
        )
        self.templates = templates

    def url(self, name):
        if name in self.templates:
            return self.templates[name]
        else:
            return name

    def config(self, name):
        r = requests.get(self.url(name))
        if r.status_code == 200:
            return r.text
        else:
            exit("Couldn't load template from %s" % self.url())


@click.group()
def cli():
    """
    knt provides a number of tools for working with Knative Build Templates.
    """
    pass


@click.command()
@click.argument("name", metavar="NAME/URL")
def install(name):
    """
    Install a BuildTempate based on short name or URL.
    Requires kubectl to be installed and configured.
    """
    repo = TemplateRepository()
    command = run(
        "kubectl.exe apply -f %s" % repo.url(name), capture_output=True, shell=True
    )
    click.echo(command.stdout.decode())


@click.command()
def list_templates():
    """
    List known BuildTemplates.
    """
    templates = []
    repo = TemplateRepository()
    for template in repo.templates:
        templates.append([template, repo.templates[template]])
    click.echo(tabulate(templates))


@click.command()
@click.argument("name", metavar="NAME/URL")
def inspect(name):
    """
    Inspect a BuildTemplate by name or URL. Shows details of parameters and arguments.
    """
    repo = TemplateRepository()
    config = yaml.load(repo.config(name))

    kind = config["kind"]
    name = config["metadata"]["name"]

    parameters = config["spec"]["parameters"]

    steps = config["spec"]["steps"]

    rows, columns = os.popen("stty size", "r").read().split()

    display_params = []
    for param in parameters:
        if "default" in param:
            default = param["default"]
        else:
            default = ""
        display_params.append(
            [
                param["name"],
                "\n".join(textwrap.wrap(param["description"], int(columns) - 20)),
                default,
            ]
        )

    steps_data = []
    steps_headers = [
        "Steps ({count})".format(count=len(steps)),
        "Image",
        "Command",
        "Args",
    ]
    for step in steps:
        data = [step["name"], step["image"]]
        if "command" in step:
            data.append("\n".join(step["command"]))
        else:
            data.append("")
        if "args" in step:
            data.append("\n".join(step["args"]))
        else:
            data.append("")
        steps_data.append(data)

    click.echo(name)
    if name in repo.templates:
        click.echo(repo.templates[name])
    click.echo()
    click.echo(
        tabulate(
            display_params,
            headers=[
                "Parameters ({count})".format(count=len(parameters)),
                "Description",
                "Default",
            ],
        )
    )
    click.echo()
    click.echo(tabulate(steps_data, headers=steps_headers))


@click.command()
@click.argument("name", metavar="NAME/URL")
def show(name):
    """
    Show YAML document for named BuildTemplate.
    """
    repo = TemplateRepository()
    click.echo(highlight(repo.config(name), YamlLexer(), TerminalTrueColorFormatter()))


cli.add_command(inspect)
cli.add_command(show)
cli.add_command(install)
cli.add_command(list_templates, name="list")

if __name__ == "__main__":
    cli()

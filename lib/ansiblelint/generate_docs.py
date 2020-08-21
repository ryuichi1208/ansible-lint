"""Utils to generate rule table .rst documentation."""
import logging

from rich import box, console
from rich.markdown import Markdown
from rich.table import Table

from ansiblelint.rules import RulesCollection

DOC_HEADER = """
.. _lint_default_rules:

Default Rules
=============

.. contents::
   :local:

Below you can see the list of default rules Ansible Lint use to evaluate playbooks and roles:

"""

_logger = logging.getLogger(__name__)


def rules_as_rst(rules: RulesCollection) -> str:
    """Return RST documentation for a list of rules."""
    r = DOC_HEADER

    for d in rules:
        if not hasattr(d, 'id'):
            _logger.warning(
                "Rule %s skipped from being documented as it does not have an `id` attribute.",
                d.__class__.__name__)
            continue

        if d.id.endswith('01'):

            section = '{} Rules ({}xx)'.format(
                    d.tags[0].title(),
                    d.id[-3:-2])
            r += f'\n\n{section}\n{ "-" * len(section) }'

        title = f"{d.id}: {d.shortdesc}"
        r += f"\n\n.. _{d.id}:\n\n{title}\n{'*' * len(title)}\n\n{d.description}"

    return r


def rules_as_rich(rules: RulesCollection) -> str:
    """Print documentation for a list of rules, returns empty string."""
    con = console.Console()
    for d in rules:
        table = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL)
        table.add_column(d.id, style="dim", width=16)
        table.add_column(Markdown(d.shortdesc))
        table.add_row("description", Markdown(d.description))
        table.add_row("version_added", d.version_added)
        table.add_row("tags", ", ".join(d.tags))
        table.add_row("severity", d.severity)
        con.print(table)

    return ""

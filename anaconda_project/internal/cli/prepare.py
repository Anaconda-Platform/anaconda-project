# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2016, Anaconda, Inc. All rights reserved.
#
# Licensed under the terms of the BSD 3-Clause License.
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
"""The ``prepare`` command configures a project to run, asking the user questions if necessary."""
from __future__ import absolute_import, print_function
from os import path

import anaconda_project.internal.cli.console_utils as console_utils
from anaconda_project.internal.cli.prepare_with_mode import prepare_with_ui_mode_printing_errors
from anaconda_project.internal.cli.project_load import load_project


def prepare_command(project_dir, ui_mode, conda_environment, command_name, all=False, refresh=False, python=None):
    """Configure the project to run.

    Returns:
        Prepare result (can be treated as True on success).
    """
    project = load_project(project_dir, save=False)

    if path.isfile(path.join(project_dir, 'requirements.txt')):  #and not path.isfile(project.project_file.filename):
        default = project.env_specs[project.default_env_spec_name]
        if not default.conda_packages and (python is not None):
            default._conda_packages = [f'python={python}']

    if console_utils.print_project_problems(project):
        return False
    if all:
        specs = project.env_specs
    else:
        specs = {conda_environment: project.env_specs.get(conda_environment)}
    result = True
    for k, v in specs.items():
        if not prepare_with_ui_mode_printing_errors(
                project, env_spec_name=k, ui_mode=ui_mode, command_name=command_name, refresh=refresh):
            result = False
    return result


def main(args):
    """Start the prepare command and return exit status code."""
    if prepare_command(args.directory, args.mode, args.env_spec, args.command, args.all, args.refresh, args.python):
        print("The project is ready to run commands.")
        print("Use `anaconda-project list-commands` to see what's available.")
        return 0
    else:
        return 1

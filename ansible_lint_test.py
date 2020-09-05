#!/usr/bin/env python

import os
import sys
import logging
from pathlib import Path

from ansiblelint import AnsibleLintRule, RulesCollection, Runner
from ansiblelint.utils import get_playbooks_and_roles

if os.environ.get("LSR_DEBUG") == "true":
    logging.getLogger().setLevel(logging.DEBUG)

class LSRole2CollectionScanner(AnsibleLintRule):
    id = '999'
    shortdesc = 'Scanner for converting LSR to collection'
    description = 'Scanner for converting LSR to collection'
    severity = 'ERROR'
    tags = []
    version_added = 'v4.1.0'

    def __init__(self, role_modules=set()):
        super(LSRole2CollectionScanner, self).__init__()
        self.role_modules = role_modules

    # use match if you need to do line based matching/scanning
    # def match(self, file, line):
    #     logging.debug(f"match: file {file} line {line}")
    #     return False

    # similar to matchtask - play is not really an entire play - it is the
    # discrete elements in the file - used when you need to scan the
    # meta/main.yml or other types of files - matchtask is better for
    # scanning tasks with actions because it gives you the information
    # about the module, arguments, etc.
    def matchplay(self, file, play):
        logging.debug(f"matchplay: file {file} play {play}")
        # look for role references
        if file["type"] == "meta":
            roles = play.get("dependencies")
            if roles:
                print(f"dependencies {roles} at {file}")
        elif "roles" in play:
            if file["type"] != "playbook":
                logging.error(f"found 'roles' with value {play['roles']} at {file}")
            else:
                print(f"roles {play['roles']} at {file}")
        elif "include_role" in play:
            print(f"include_role {play['include_role']['name']} at {file}")
        elif "import_role" in play:
            print(f"import_role {play['import_role']['name']} at {file}")

        return False

    # use this when you need detailed information about tasks
    def matchtask(self, file, task):
        logging.debug(f"matchtask: file {file} task {task}")
        if self.role_modules and file["path"].find("/tests/") > -1 and "action" in task:
            modname = task["action"]["__ansible_module__"]
            if modname and modname in self.role_modules:
                print(f"found role module {modname} at {file}")
        return False

        # if task["action"]["__ansible_module__"] != "shell":
        #     return False

        # if task.get("ignore_errors"):
        #     return False

        # unjinjad_cmd = self.unjinja(
        #     ' '.join(task["action"].get("__ansible_arguments__", [])))

        # return (self._pipe_re.search(unjinjad_cmd) and
        #         not self._pipefail_re.match(unjinjad_cmd))


def get_role_playbooks_subroles_modules(role_path):
    """Return a list of roles, playbooks, and subroles from the given role path"""
    class Options(object):
        def __init__(self, d):
            self.__dict__ = d
    opts = Options({"exclude_paths": [], "verbosity": False})
    cwd = os.getcwd()
    os.chdir(role_path)
    # this returns only playbooks and sub-role directories
    # this adds "." since it works in cwd - we have to replace
    # that with role_path
    role_pbs = set()
    for ff in get_playbooks_and_roles(opts):
        if ff == ".":
            role_pbs.add(role_path)
        else:
            role_pbs.add(os.path.join(role_path, ff))
    role_modules = set()
    library_path = Path("library")
    if library_path.is_dir():
        for mod_file in library_path.iterdir():
            if mod_file.is_file() and mod_file.stem != "__init__":
                role_modules.add(mod_file.stem)
    os.chdir(cwd)
    return role_pbs, role_modules


def use_ansible_lint():
    # assume args are lsr role directories
    for role_path in sys.argv[1:]:
        role_pbs, role_modules = get_role_playbooks_subroles_modules(role_path)
        role_pbs = sorted(role_pbs)
        rules = RulesCollection()
        rules.register(LSRole2CollectionScanner(role_modules))
        tags = []
        skip_list = frozenset([])
        role_name = Path(role_path).stem
        exclude_paths = [
            os.path.join(role_path, ".tox"),
            os.path.join(role_path, ".venv"),
            os.path.join(role_path, "tests", "roles", role_name),
            os.path.join(role_path, "tests", "roles", f"linux-system-roles.{role_name}"),
            os.path.join(role_path, "tests", "playbooks", "roles", role_name),
            os.path.join(role_path, "tests", "playbooks", "roles", f"linux-system-roles.{role_name}"),
        ]
        for role_or_pb in role_pbs:
            runner = Runner(rules, role_or_pb, tags, skip_list, exclude_paths)
            # runner = Runner(rules, playbook, options.tags,
            #                 options.skip_list, options.exclude_paths,
            #                 options.verbosity, checked_files)
            runner.run()


def use_ansible_lint_get_pb_and_roles():
    from ansiblelint.utils import get_playbooks_and_roles
    class Options(object):
        def __init__(self, d):
            self.__dict__ = d

    cwd = os.getcwd()
    opts = Options({"exclude_paths": [], "verbosity": False})
    for role_dir in sys.argv[1:]:
        os.chdir(role_dir)
        # this returns only playbooks and sub-role directories
        result = get_playbooks_and_roles(opts)
    os.chdir(cwd)


def use_ansible(filepath):
    from ansible import constants
    from ansible.errors import AnsibleError
    from ansible.errors import AnsibleParserError
    from ansible.parsing.dataloader import DataLoader
    from ansible.parsing.mod_args import ModuleArgsParser
    from ansible.parsing.splitter import split_args
    from ansible.parsing.yaml.constructor import AnsibleConstructor
    from ansible.parsing.yaml.loader import AnsibleLoader
    from ansible.parsing.yaml.objects import AnsibleSequence
    from ansible.plugins.loader import module_loader
    dl = DataLoader()
    return dl.load_from_file(filepath)


use_ansible_lint()

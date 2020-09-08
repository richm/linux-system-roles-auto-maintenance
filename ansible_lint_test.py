#!/usr/bin/env python

import os
import sys
import logging
from pathlib import Path

import ansiblelint
from ansiblelint import AnsibleLintRule, RulesCollection, Runner
import ansiblelint.utils
from ansiblelint.utils import get_playbooks_and_roles, find_children

if os.environ.get("LSR_DEBUG") == "true":
    logging.getLogger().setLevel(logging.DEBUG)

# monkeypatch find_children to fix this issue:
# WARNING: Couldn't open /home/rmeggins/working/lsr/network/tests/playbooks/tasks/tasks/show_interfaces.yml - No such file or directory
# I guess ansible-lint doesn't use the same relative path resolution mechanism that ansible uses
orig_find_children = ansiblelint.utils.find_children
def fix_find_children(playbook, playbook_dir):
    results = []
    for child in orig_find_children(playbook, playbook_dir):
        child["path"] = child["path"].replace("tasks/tasks/", "tasks/")
        results.append(child)
    return results
ansiblelint.utils.find_children = fix_find_children

# monkeypatch _append_skipped_rules to fix this issue:
# Error trying to append skipped rules: RuntimeError('Unexpected file type: pre_tasks')
orig___append_skipped_rules = ansiblelint.utils._append_skipped_rules
def fix__append_skipped_rules(pyyaml_data, file_text, file_type):
    new_file_type = file_type
    if file_type in ["pre_tasks", "post_tasks"]:
        new_file_type = "tasks"
    return orig___append_skipped_rules(pyyaml_data, file_text, new_file_type)
ansiblelint.utils._append_skipped_rules = fix__append_skipped_rules

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
    return role_pbs, role_modules


def use_ansible_lint():
    # assume args are lsr role directories
    for role_path in sys.argv[1:]:
        cwd = os.getcwd()
        os.chdir(role_path)
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
            os.path.join(role_path, "examples", "roles", role_name),
            os.path.join(role_path, "examples", "roles", f"linux-system-roles.{role_name}"),
        ]
        for role_or_pb in role_pbs:
            runner = Runner(rules, role_or_pb, tags, skip_list, exclude_paths)
            # runner = Runner(rules, playbook, options.tags,
            #                 options.skip_list, options.exclude_paths,
            #                 options.verbosity, checked_files)
            runner.run()
        os.chdir(cwd)


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

ROLE_DIRS = ["defaults", "examples", "files", "handlers", "library", "meta",
    "module_utils", "tasks", "templates", "tests", "vars"]

def is_role_dir(role_path, dirpath):
    if role_path == dirpath:
        return False
    dir_pth = Path(dirpath)
    relpath = dir_pth.relative_to(role_path)
    base_dir = relpath.parts[0]
    return base_dir in ROLE_DIRS

PLAY_KEYS = {
    "gather_facts",
    "handlers",
    "hosts",
    "import_playbook",
    "post_tasks",
    "pre_tasks",
    "roles"
    "tasks",
}

import codecs
from ansible import constants
from ansible.errors import AnsibleError
from ansible.errors import AnsibleParserError
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.mod_args import ModuleArgsParser
from ansible.parsing.splitter import split_args
from ansible.parsing.yaml.constructor import AnsibleConstructor
from ansible.parsing.yaml.loader import AnsibleLoader
from ansible.parsing.yaml.objects import AnsibleSequence, AnsibleMapping
from ansible.plugins.loader import module_loader

def get_file_type(item):
    if isinstance(item, AnsibleMapping):
        if "galaxy_info" in item or "dependencies" in item:
            return "meta"
        return "vars"
    elif isinstance(item, AnsibleSequence):
        return "tasks"
    else:
        raise Exception(f"Error: unknown type of file: {item}")


def get_item_type(item):
    if isinstance(item, AnsibleMapping):
        for key in PLAY_KEYS:
            if key in item:
                return "play"
        if "block" in item:
            return "block"
        return "task"
    else:
        raise Exception(f"Error: unknown type of item: {item}")

def handle_other(item):
    """handle properties of Ansible item other than vars and tasks"""
    return

def handle_vars(item):
    """handle vars of Ansible item"""
    for var in item.get("vars", []):
        print(f"\tvar = {var}")
    return

def handle_meta(item):
    """handle meta/main.yml file"""
    print(f"\tmeta dependencies {item.get('dependencies')}")

def handle_task(task):
    """handle a single task"""
    mod_arg_parser = ModuleArgsParser(task)
    try:
        action, arguments, _ = mod_arg_parser.parse(skip_action_validation=True)
    except AnsibleParserError as e:
        raise SystemExit("Couldn't parse task at %s (%s)\n%s" % (task, e.message, task))
    print(f"\ttask action {action} args {arguments}")
    handle_tasks(task)

def handle_task_list(tasks):
    """item is a list of Ansible Task objects"""
    for task in tasks:
        if "block" in task:
            handle_tasks(task)
        else:
            handle_task(task)
    
def handle_tasks(item):
    """item has one or more fields which hold a list of Task objects"""
    if "always" in item:
        handle_task_list(item["always"])
    if "block" in item:
        handle_task_list(item["block"])
    if "handlers" in item:
        handle_task_list(item["post_tasks"])
    if "pre_tasks" in item:
        handle_task_list(item["pre_tasks"])
    if "post_tasks" in item:
        handle_task_list(item["post_tasks"])
    if "rescue" in item:
        handle_task_list(item["rescue"])
    if "tasks" in item:
        handle_task_list(item["tasks"])

def use_ansible():
    role_path = sys.argv[1]
    for (dirpath, _, filenames) in os.walk(role_path):
        if not is_role_dir(role_path, dirpath):
            continue
        for filename in filenames:
            if not filename.endswith(".yml"):
                continue
            filepath = os.path.join(dirpath, filename)
            print(f"filepath {filepath}")
            dl = DataLoader()
            ans_data = dl.load_from_file(filepath)
            file_type = get_file_type(ans_data)
            if file_type == "vars":
                handle_vars(item)
                continue
            if file_type == "meta":
                handle_meta(item)
                continue
            for item in ans_data:
                ans_type = get_item_type(item)
                handle_tasks(item)
                handle_vars(item)
                handle_other(item)
                if ans_type == "task":
                    handle_task(item)

use_ansible()

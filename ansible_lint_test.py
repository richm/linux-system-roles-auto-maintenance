#!/usr/bin/env python

import os
import sys
import logging
from pathlib import Path

from ansible.errors import AnsibleParserError
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.mod_args import ModuleArgsParser
from ansible.parsing.yaml.objects import AnsibleSequence, AnsibleMapping

if os.environ.get("LSR_DEBUG") == "true":
    logging.getLogger().setLevel(logging.DEBUG)


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
    for role in item.get("roles", []):
        print(f"\troles item role {role}")
    return

def handle_vars(item):
    """handle vars of Ansible item"""
    for var in item.get("vars", []):
        print(f"\tvar = {var}")
    return

def handle_meta(item):
    """handle meta/main.yml file"""
    for role in item.get("dependencies", []):
        print(f"\tmeta dependencies role {role}")

def handle_task(task):
    """handle a single task"""
    mod_arg_parser = ModuleArgsParser(task)
    try:
        action, _, _ = mod_arg_parser.parse(skip_action_validation=True)
    except AnsibleParserError as e:
        raise SystemExit("Couldn't parse task at %s (%s)\n%s" % (task, e.message, task))
    if action == "include_role" or action == "import_role":
        print(f"\ttask role {task[action]['name']}")
    elif action in role_modules:
        print(f"\ttask role module {action}")
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

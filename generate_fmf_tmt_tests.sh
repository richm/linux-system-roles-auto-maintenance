#!/bin/bash

set -euo pipefail

PLANS_DIR="${PLANS_DIR:-tests/tmt_plans}"

if [ "${DEBUG:-false}" = true ];
    set -x
fi

if [ ! -d .fmf ]; then
    mkdir .fmf
fi

if [ ! -f .fmf/version ]; then
    echo "1" > .fmf/version
fi

if [ ! -d "$PLANS_DIR" ]; then
    mkdir -p "$PLANS_DIR"
fi

if [ ! -f .packit.yaml ]; then
    cat > .packit.yaml <<EOF
jobs:
- job: tests
  skip_build: true
  trigger: pull_request
  targets:
  - fedora-latest-stable
  - epel-8
EOF
fi

create_plan() {
    local planname collection use_collection ansible_ver
    planname="$1"
    use_collection="$2"
    ansible_ver="$3"
    if [ "$use_collection" = true ]; then
        collection="_collection"
    else
        collection=""
    fi
    cat > "$PLANS_DIR/${planname}${collection}_${ansible_ver}" <<EOF
summary: ${planname}${collection}
environment:
  LSR_TEST_PB: ${planname}.yml
  ANSIBLE_VENV: /tmp/.venv
  USE_COLLECTION: "${use_collection}"
prepare:
  - how: shell
    script: |
      set -euxo pipefail
      yum_dnf=yum
      if type -p dnf; then
        yum_dnf=dnf
      fi
      PKGS="python3-pip python3-virtualenv python3-setuptools openssl curl python3-ruamel-yaml"
      "\$yum_dnf" install -y \$PKGS
      PIP_PKGS="ansible==${ansible_ver}.*"
      . /etc/os-release
      case "\$ID" in
      centos|rhel) if [ "\$VERSION_ID" -le 8 ]; then
                     PIP_PKGS="\$PIP_PKGS jinja2==2.7.*"
                   fi ;;
      esac
      python3 -mvenv "$ANSIBLE_VENV"
      . "$ANSIBLE_VENV/bin/activate"
      pip install \$PIP_PKGS
execute:
  script: |
    . "$ANSIBLE_VENV/bin/activate"
    ansible --version
    curl -o /tmp/run_test_pb_localhost.sh https://raw.githubusercontent.com/richm/tox-lsr/basic-smoke-test/src/tox_lsr/test_scripts/run_test_pb_localhost.sh
    bash -x /tmp/run_test_pb_localhost.sh
EOF
}

for file in tests/tests_*.yml; do
    testname="$(basename "$file" .yml)"
    create_plan "$testname" false 2.9
    create_plan "$testname" true 2.9
    create_plan "$testname" false 2.13
    create_plan "$testname" true 2.13
done

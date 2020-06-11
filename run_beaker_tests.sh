#!/bin/bash

set -euo pipefail

usage() {
  cat <<EOF
Usage: $0 URL control_host_distro control_host_version control_host_arch managed_host_distro managed_host_version managed_host_arch [[managed_host_distro managed_host_version managed_host_arch] ...]
This will submit a beaker job to:
* provision the control host and managed hosts
* download the url on the control host
* run the tests against the managed hosts
EOF
}

# email address to use for beaker reservation
BKR_EMAIL=${BKR_EMAIL:-"$USER@redhat.com"}
# time in seconds to reserve the machines
BKR_RESERVE_TIME=${BKR_RESERVE_TIME:-86400}
# number of attempts to take to successfully submit a single job
BKR_JOB_TRIES=20
# time in seconds to wait for job to progress before retry
# based on recent impirical observation, seems to take less than
# 15 minutes for installation to start if everything is working
BKR_JOB_TIMEOUT=900
# time in seconds to wait after job-clone/submit before checking status
BKR_JOB_DELAY=5
# result checking period in seconds
BKR_CHECK_PERIOD=15

CONTROLLER_PKGS="screen git curl ansible"
MANAGED_PKGS="screen"

bkr_job_file=$(mktemp lsr_bkr_job_XXXXXXXXX.xml)
bkr_status_file=$(mktemp lsr_bkr_status_XXXXXXXXX.xml)
bkr_ansible_ssh_key=$(mktemp lsr_bkr_key_lsr_bkr_job_XXXXXXXXX.key)
bkr_ansible_ssh_pubkey=${bkr_ansible_ssh_key}.pub
trap 'rm -f $bkr_job_file $bkr_ansible_ssh_key $bkr_ansible_ssh_pubkey $bkr_status_file' EXIT

# this is to be run on the control host to get the list of managed hosts
# to feed into ansible
get_managed_hosts() {
  local recipe_xml
  recipe_xml=$(mktemp lsr_recipe_XXXXXXXXX.xml)
  curl -s -o "$recipe_xml" "$BEAKER_LAB_CONTROLLER_URL/recipes/$BEAKER_RECIPE_ID/"
  xmllint --xpath 'string(/job/recipeSet/recipe/roles/role[@value="MANAGED_HOST"]/system/@value)' "$recipe_xml"
  rm -f "$recipe_xml"
}

# family - is ${PRODUCT}${VERSION}
# where PRODUCT is one of CentOS (version 7 and earlier), CentOSLinux, RedHatEnterpriseLinux, Fedora
# where VERSION is typically the major version, or "rawhide" for Fedora
# examples of family:
# RedHatEnterpriseLinux8, CentOS7, CentOSLinux8, Fedora32, Fedorarawhide
# for distro - it is best to look up the actual distro string for the family
# bkr distros-list --limit=0 --family=$name e.g.
# bkr distros-list --limit=0 --family=Fedora31
#        ID: 11277
#      Name: Fedora-31
# OSVersion: Fedora31.0
#      Tags: RELEASED
# so use the Name field - Fedora-31 - as the distro_name
# for RHEL - the Distro will usually be a long string like
# RHEL-8.3.0-20200526.n.1
# use a query like this:
# bkr distro-trees-list --limit=0 --family=$family_name --format=json | jq -r '.[]|.distro_osmajor + " " + .arch + " " + .distro_name + " " + .distro_osversion'
# to see a list of all of the arch and distro_name values available for a given family

make_job_header() {
  cat <<EOF
<job>
  <whiteboard>
    ${BKR_WHITEBOARD_STRING:-Beaker job for Linux System Roles testing - take 4 - take 3 failed, controller timed out}
  </whiteboard>
  <recipeSet>
EOF
}

make_ks_appends_managed() {
  cat <<EOF
        <ks_appends>
          <ks_append><![CDATA[
%post
if [ ! -d /root/.ssh ]; then
  mkdir -p /root/.ssh
fi
echo "$(cat $bkr_ansible_ssh_pubkey)" >> /root/.ssh/authorized_keys
%end
          ]]></ks_append>
        </ks_appends>
EOF
}

make_ks_appends_control() {
  cat <<EOF
        <ks_appends>
          <ks_append><![CDATA[
%post
if [ ! -d /root/.ssh ]; then
    mkdir -p /root/.ssh
fi
chmod 0700 /root/.ssh
echo "$(cat $bkr_ansible_ssh_key)" > /root/.ssh/id_rsa
chmod 0400 /root/.ssh/id_rsa
echo "$(cat $bkr_ansible_ssh_pubkey)" > /root/.ssh/id_rsa.pub
chmod 0400 /root/.ssh/id_rsa.pub
echo UpdateHostKeys yes > /root/.ssh/config
echo UserKnownHostsFile /dev/null >> /root/.ssh/config
echo StrictHostKeyChecking no >> /root/.ssh/config
echo PasswordAuthentication no >> /root/.ssh/config
chmod 0600 /root/.ssh/config
%end
          ]]></ks_append>
        </ks_appends>
EOF
}

make_recipe() {
  local role=$1
  local family=Fedora31
  local distro=Fedora-31
  local arch=x86_64
  local variant=Server
  local pkgs
  local pkg
  cat <<EOF
    <recipe role="$role" whiteboard="$role host">
EOF
  if [ "$role" = SERVERS ]; then
    make_ks_appends_managed
    pkgs="$MANAGED_PKGS"
  else # assume control host
    make_ks_appends_control
    pkgs="$CONTROLLER_PKGS"
  fi
  cat <<EOF
      <packages>
EOF
  for pkg in $pkgs; do
    echo "        <package name=\"$pkg\"/>"
  done
  cat <<EOF
      </packages>
      <distroRequires>
        <and>
          <distro_family op="=" value="$family"/>
          <distro_variant op="=" value="$variant"/>
          <distro_name op="=" value="$distro"/>
          <distro_arch op="=" value="$arch"/>
        </and>
      </distroRequires>
      <hostRequires>
        <system_type value="Machine"/>
      </hostRequires>
      <task name="/distribution/check-install" role="STANDALONE"/>
      <task name="/distribution/command" role="STANDALONE">
EOF
  if [ "$role" = SERVERS ]; then
    cat <<EOF
        <params>
          <param name="CMDS_TO_RUN" value="echo hello from $role host"/>
        </params>
EOF
  else
    cat <<EOF
        <params>
          <param name="CMDS_TO_RUN" value="ansible -i \${SERVERS}, -m setup all"/>
        </params>
EOF
  fi
    cat <<EOF
      </task>
      <task role="STANDALONE" name="/distribution/reservesys">
        <params>
          <param name="RESERVEBY" value="$BKR_EMAIL"/>
          <param name="RESERVETIME" value="$BKR_RESERVE_TIME"/>
        </params>
      </task>
    </recipe>
EOF
}

make_job_footer() {
  cat <<EOF
  </recipeSet>
</job>
EOF
}

make_ssh_key() {
  # on Fedora 31 this prompts:
  # filexxxx already exists.  Overwrite (y/n)?
  # even though the file does not exist - so have to add the echo y
  echo y | ssh-keygen -C "for LSR ansible testing" -q -N "" -V -1h:+3h -f "$bkr_ansible_ssh_key" > /dev/null
}

get_job_status() {
  local jobid="$1"
  bkr job-results --prettyxml "$jobid"
}

get_task_statuses() {
  local statusfile="$1"
  xmllint --xpath '//task[@name="/distribution/check-install"]/@status' "$statusfile" | \
    sed 's/^.*status="\([^"][^"]*\)".*$/\1/'
}

# returns true if all recipes have started installation
# if the xpath query returns no count, assume installation has not started
is_installation_started() {
  local statusfile="$1"
  local count
  count=$(xmllint --xpath 'count(//installation[not(@install_started)])' "$statusfile")
  test "${count:-99}" = 0
}

# control and managed are given as
# DISTRO : ARCH
# e.g.
# Fedora31:x86_64 RHEL-8.2.1-20200529.n.1:aarch64
# If DISTRO is a family, the latest distro for that family will be used
# If DISTRO is an osversion e.g. RedHatEnterpriseLinux8.2, the latest
# distro for that osversion will be used

# managed_list=""
# while [ -n "${1:-}" ]; do
#     case "$1" in
#     --control) shift; control="$1";;
#     --managed) shift; managed_list="$managed_list $1";;
#     --url) shift; url="$1";;
#     *) usage; exit 1;;
#     esac
#     shift
# done

# validate_input

# control_distro=$(get_distro $control)
# control_arch=$(get_arch $control)

make_new_job() {
  make_job_header
  make_recipe SERVERS
  make_recipe CLIENTS
  make_job_footer
}

status_is_error() {
  [ "$1" = "Aborted" ] || [ "$1" = "Cancelled" ]
}

status_is_incomplete() {
  [ "$1" = "New" ] || [ "$1" = "Processed" ] || [ "$1" = "Scheduled" ] || [ "$1" = "Waiting" ] || [ "$1" = "Queued" ]
}

make_ssh_key
failed=
for try in $(seq 1 "$BKR_JOB_TRIES"); do
#DEBUG="--dry-run --xml"
# output looks like this: Submitted: ['J:4328568']
  if [ -z "${jobid:-}" ]; then
    make_new_job > "$bkr_job_file"
    output=$(bkr job-submit ${DEBUG:-} "$bkr_job_file" 2>&1)
    sleep "$BKR_JOB_DELAY"
  else
    output=$(bkr job-clone ${DEBUG:-} "$jobid" 2>&1)
    sleep "$BKR_JOB_DELAY"
    bkr job-cancel "$jobid"
    (sleep 30 ; bkr job-delete "$jobid") &
  fi
  echo "$output"
  jobid=$(echo "$output" | sed "s/^.*\['\([^'][^']*\)'\].*$/\1/")
  ii="${BKR_JOB_TIMEOUT}"
  while [ $ii -gt 0 ]; do
    get_job_status "$jobid" > "$bkr_status_file"
    if is_installation_started "$bkr_status_file"; then
      status=started
      failed=
      break
    fi
    for status in $(get_task_statuses "$bkr_status_file"); do
      if status_is_error "$status"; then
        break
      fi
      if status_is_incomplete "$status"; then
        break
      fi
    done
    if status_is_incomplete "$status"; then
      echo "try $try job $jobid status $status time remaining $ii"
      sleep "$BKR_CHECK_PERIOD"
      ii=$((ii - BKR_CHECK_PERIOD)) || :
      continue
    fi
    if status_is_error "$status"; then
      break
    else
      echo "try $try unknown status $status jobid $jobid time remaining $ii"
      break
    fi
  done
  if is_installation_started "$bkr_status_file"; then
    status=started
    failed=
    break
  fi
  if status_is_incomplete "$status"; then
    echo "try $try - Still waiting after 10 minutes - will clone job $jobid"
    failed=true
  elif status_is_error "$status"; then
    echo "try $try - One or more tasks was aborted - will clone job $jobid"
    failed=true
  else
    failed=
    break
  fi
  bkr job-results --prettyxml "$jobid"
done

if [ "${failed:-}" = true ]; then
  echo "Job failed to start installation after $try retries"
  exit 1
fi
echo "Looks like job $jobid will be successful"

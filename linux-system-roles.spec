%if 0%{?rhel}
Name: rhel-system-roles
%else
Name: linux-system-roles
%endif
Summary: Set of interfaces for unified system management
Version: 1.0
Release: 20%{?dist}

#Group: Development/Libraries
License: GPLv3+ and MIT and BSD
%if 0%{?rhel}
%global rolealtprefix linux-system-roles.
%endif
%global roleprefix %{name}.

# For each role, call either defcommit() or deftag(). The other macros
# (%%id and %%shortid) can be then used in the same way in both cases.
# This way  the rest of the spec file des not need to know whether we are
# dealing with a tag or a commit.
%define defcommit() %{expand:%%global id%{1} %{2}
%%global shortid%{1} %%(c=%%{id%{1}}; echo ${c:0:7})
}

%define deftag() %{expand:%%global id%{1} %{2}
%%global shortid%{1} %{2}
}

%defcommit 0 0c2bb286bbc1b73d728226924e0010c0fa1ce30a
%global rolename0 kdump
#%%deftag 0 1.0.0

#%%defcommit 1 43eec5668425d295dce3801216c19b1916df1f9b
%global rolename1 postfix
%deftag 1 0.1

%defcommit 2 6cd1ec8fdebdb92a789b14e5a44fe77f0a3d8ecd
%global rolename2 selinux
#%%deftag 2 1.0.0

%defcommit 3 924650d0cd4117f73a7f0413ab745a8632bc5cec
%global rolename3 timesync
#%%deftag 3 1.0.0

%defcommit 5 bf4501bb8770d3ef761e1684011c905f99a9752f
%global rolename5 network
#%%deftag 5 1.0.0

%defcommit 6 81f30ab336f4ecc61b4a30ffcb080e17fd35de2e
%global rolename6 storage
#%%deftag 6 1.0.2

%defcommit 7 7f94b49688902eb507e0ebeda1fbf08621bc3c6b
%global rolename7 metrics
#%%deftag 7 0.1.0

%defcommit 8 cfa70b6b5910b3198aba2679f8fc36aad45ca45a
%global rolename8 tlog
#%%deftag 8 0.2.0

%defcommit 9 901a73a4285469ef50a6cc37135ae55ce9d2e41b
%global rolename9 kernel_settings
#%%deftag 9 0.2.0

%defcommit 10 fe3f658e72b2883d2a1460d453105c7a53dd70e8
%global rolename10 logging
#%%deftag 10 0.2.0

%defcommit 11 4b6cfca4dd24e53a4bc4e07635601d7c104346c1
%global rolename11 nbde_server
#%%deftag 11 0.1.0

%defcommit 12 6306defad146d8274b04f438a04e17e44672f1a6
%global rolename12 nbde_client
#%%deftag 12 0.1.0

%defcommit 13 fedef6e7844bb623bb54695a602137e332f5509f
%global rolename13 certificate
#%%deftag 13 0.1.0

Source: https://github.com/linux-system-roles/%{rolename0}/archive/%{id0}.tar.gz#/%{rolename0}-%{shortid0}.tar.gz
Source1: https://github.com/linux-system-roles/%{rolename1}/archive/%{id1}.tar.gz#/%{rolename1}-%{shortid1}.tar.gz
Source2: https://github.com/linux-system-roles/%{rolename2}/archive/%{id2}.tar.gz#/%{rolename2}-%{shortid2}.tar.gz
Source3: https://github.com/linux-system-roles/%{rolename3}/archive/%{id3}.tar.gz#/%{rolename3}-%{shortid3}.tar.gz
Source5: https://github.com/linux-system-roles/%{rolename5}/archive/%{id5}.tar.gz#/%{rolename5}-%{shortid5}.tar.gz
Source6: https://github.com/linux-system-roles/%{rolename6}/archive/%{id6}.tar.gz#/%{rolename6}-%{shortid6}.tar.gz
Source7: https://github.com/linux-system-roles/%{rolename7}/archive/%{id7}.tar.gz#/%{rolename7}-%{shortid7}.tar.gz
Source8: https://github.com/linux-system-roles/%{rolename8}/archive/%{id8}.tar.gz#/%{rolename8}-%{shortid8}.tar.gz
Source9: https://github.com/linux-system-roles/%{rolename9}/archive/%{id9}.tar.gz#/%{rolename9}-%{shortid9}.tar.gz
Source10: https://github.com/linux-system-roles/%{rolename10}/archive/%{id10}.tar.gz#/%{rolename10}-%{shortid10}.tar.gz
Source11: https://github.com/linux-system-roles/%{rolename11}/archive/%{id11}.tar.gz#/%{rolename11}-%{shortid11}.tar.gz
Source12: https://github.com/linux-system-roles/%{rolename12}/archive/%{id12}.tar.gz#/%{rolename12}-%{shortid12}.tar.gz
Source13: https://github.com/linux-system-roles/%{rolename13}/archive/%{id13}.tar.gz#/%{rolename13}-%{shortid13}.tar.gz

%global mainid 0.0.1
Source100: https://github.com/pcahyna/auto-maintenance/archive/%{mainid}.tar.gz#/auto-maintenance-%{mainid}.tar.gz

Source999: md2html.sh

%if "%{roleprefix}" != "linux-system-roles."
Patch1: rhel-system-roles-%{rolename1}-prefix.diff
Patch2: rhel-system-roles-%{rolename2}-prefix.diff
Patch3: rhel-system-roles-%{rolename3}-prefix.diff
Patch5: rhel-system-roles-%{rolename5}-prefix.diff
Patch6: rhel-system-roles-%{rolename6}-prefix.diff
# for some roles, the prefix change can be scripted - see below
%endif

# Patch11: rhel-system-roles-postfix-pr5.diff
# Patch12: postfix-meta-el8.diff
# Patch101: rhel-system-roles-kdump-pr22.diff

# Patch102: kdump-tier1-tags.diff
# Patch103: kdump-meta-el8.diff

# Patch21: selinux-tier1-tags.diff

# Patch31: timesync-tier1-tags.diff

# Patch52: network-permissions.diff
# Patch53: network-tier1-tags.diff

# Patch61: storage-safemode-luks.diff

Url: https://github.com/linux-system-roles/
BuildArch: noarch

BuildRequires: asciidoc
BuildRequires: pandoc
BuildRequires: highlight

Requires: python3-jmespath

Obsoletes: rhel-system-roles-techpreview < 1.0-3

# We need to put %%description within the if block to avoid empty
# lines showing up.
%if 0%{?rhel}
%description
Collection of Ansible roles and modules that provide a stable and
consistent configuration interface for managing multiple versions
of Red Hat Enterprise Linux.
%else
%description
Collection of Ansible roles and modules that provide a stable and
consistent configuration interface for managing multiple versions
of Fedora, Red Hat Enterprise Linux & CentOS.
%endif

%prep
%setup -qc -a1 -a2 -a3 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13
cd %{rolename0}-%{id0}
#%%patch101 -p1
#%%patch102 -p1
#%%patch103 -p1
cd ..
cd %{rolename1}-%{id1}
%if "%{roleprefix}" != "linux-system-roles."
%patch1 -p1
%endif
#%%patch11 -p1
#%%patch12 -p1
cd ..
cd %{rolename2}-%{id2}
%if "%{roleprefix}" != "linux-system-roles."
%patch2 -p1
%endif
#%%patch21 -p1
cd ..
cd %{rolename3}-%{id3}
%if "%{roleprefix}" != "linux-system-roles."
%patch3 -p1
%endif
#%%patch31 -p1
cd ..
cd %{rolename5}-%{id5}
%if "%{roleprefix}" != "linux-system-roles."
%patch5 -p1
%endif
#%%patch52 -p1
#%%patch53 -p1
cd ..
cd %{rolename6}-%{id6}
%if "%{roleprefix}" != "linux-system-roles."
%patch6 -p1
%endif
#%%patch61 -p1
cd ..

# for some roles, the prefix change can be scripted - see below
%if "%{roleprefix}" != "linux-system-roles."
for rolename_id in %{rolename7}-%{id7} %{rolename8}-%{id8} %{rolename9}-%{id9} \
    %{rolename10}-%{id10} %{rolename11}-%{id11} %{rolename12}-%{id12} \
    %{rolename13}-%{id13}; do
    # assumes rolename has no dash in it
    # note that we have to use double %%
    # in order for a single % to be passed to bash
    rolename=${rolename_id%%-*}
    find $rolename_id -type f -exec \
         sed "s/linux-system-roles[.]${rolename}\\>/%{roleprefix}${rolename}/g" -i {} \;
done
%endif

%build
sh %{SOURCE999} \
%{rolename0}-%{id0}/README.md \
%{rolename1}-%{id1}/README.md \
%{rolename2}-%{id2}/README.md \
%{rolename3}-%{id3}/README.md \
%{rolename5}-%{id5}/README.md \
%{rolename6}-%{id6}/README.md \
%{rolename7}-%{id7}/README.md \
%{rolename8}-%{id8}/README.md \
%{rolename9}-%{id9}/README.md \
%{rolename10}-%{id10}/README.md \
%{rolename11}-%{id11}/README.md \
%{rolename12}-%{id12}/README.md \
%{rolename13}-%{id13}/README.md

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles

cp -pR %{rolename0}-%{id0}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename0}
cp -pR %{rolename1}-%{id1}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename1}
cp -pR %{rolename2}-%{id2}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename2}
cp -pR %{rolename3}-%{id3}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename3}
cp -pR %{rolename5}-%{id5}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename5}
cp -pR %{rolename6}-%{id6}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename6}
cp -pR %{rolename7}-%{id7}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename7}
cp -pR %{rolename8}-%{id8}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename8}
cp -pR %{rolename9}-%{id9}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename9}
cp -pR %{rolename10}-%{id10}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename10}
cp -pR %{rolename11}-%{id11}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename11}
cp -pR %{rolename12}-%{id12}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename12}
cp -pR %{rolename13}-%{id13}      $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}%{rolename13}

%if 0%{?rolealtprefix:1}
ln -s    %{roleprefix}%{rolename0}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename0}
ln -s    %{roleprefix}%{rolename1}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename1}
ln -s    %{roleprefix}%{rolename2}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename2}
ln -s    %{roleprefix}%{rolename3}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename3}
ln -s    %{roleprefix}%{rolename5}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename5}
ln -s    %{roleprefix}%{rolename6}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename6}
ln -s    %{roleprefix}%{rolename7}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename7}
ln -s    %{roleprefix}%{rolename8}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename8}
ln -s    %{roleprefix}%{rolename9}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename9}
ln -s    %{roleprefix}%{rolename10}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename10}
ln -s    %{roleprefix}%{rolename11}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename11}
ln -s    %{roleprefix}%{rolename12}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename12}
ln -s    %{roleprefix}%{rolename13}   $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}%{rolename13}
%endif

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/kdump
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/postfix
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/selinux
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/timesync
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/network
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/storage
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/metrics
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/tlog
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/kernel_settings
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/logging
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/nbde_server
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/nbde_client
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/certificate

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}kdump/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}kdump/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}kdump/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/kdump

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}postfix/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}postfix/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}postfix/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/postfix

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}selinux/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}selinux/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}selinux/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/selinux
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}selinux/selinux-playbook.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/selinux/example-selinux-playbook.yml

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}timesync/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}timesync/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}timesync/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/timesync
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}timesync/examples/multiple-ntp-servers.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/timesync/example-timesync-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}timesync/examples/single-pool.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/timesync/example-timesync-pool-playbook.yml

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/LICENSE \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/bond_with_vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-bond_with_vlan-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/bridge_with_vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-bridge_with_vlan-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/eth_simple_auto.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth_simple_auto-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/eth_with_vlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth_with_vlan-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/infiniband.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-infiniband-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/macvlan.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-macvlan-playbook.yml
cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/remove_profile.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-remove_profile-playbook.yml
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/remove_profile.yml
cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/down_profile.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-down_profile-playbook.yml
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/down_profile.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/inventory \
   $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-inventory
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/ethtool_features.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-ethtool_features-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/ethtool_features_default.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-ethtool_features_default-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/bond_simple.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-bond_simple-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/eth_with_802_1x.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-eth_with_802_1x-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/wireless_wpa_psk.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-wireless_wpa_psk-playbook.yml
mv $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/remove+down_profile.yml \
    $RPM_BUILD_ROOT%{_pkgdocdir}/network/example-remove+down_profile-playbook.yml

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}storage/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}storage/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}storage/LICENSE \
    $RPM_BUILD_ROOT%{_pkgdocdir}/storage

rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}*/semaphore
rm -r $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}*/molecule
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}*/.travis.yml
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}*/.ansible-lint

rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/.gitignore
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/tests/.gitignore
rm $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples/roles
rmdir $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}network/examples

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}metrics/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}metrics/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}metrics/LICENSE \
    $RPM_BUILD_ROOT%{_pkgdocdir}/metrics

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}tlog/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}tlog/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}tlog/LICENSE \
    $RPM_BUILD_ROOT%{_pkgdocdir}/tlog

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}kernel_settings/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}kernel_settings/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}kernel_settings/LICENSE \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}kernel_settings/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/kernel_settings

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}logging/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}logging/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}logging/LICENSE \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}logging/COPYING \
    $RPM_BUILD_ROOT%{_pkgdocdir}/logging

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}nbde_server/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}nbde_server/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}nbde_server/LICENSE \
    $RPM_BUILD_ROOT%{_pkgdocdir}/nbde_server

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}nbde_client/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}nbde_client/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}nbde_client/LICENSE \
    $RPM_BUILD_ROOT%{_pkgdocdir}/nbde_client

cp -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}certificate/README.md \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}certificate/README.html \
    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}certificate/LICENSE \
    $RPM_BUILD_ROOT%{_pkgdocdir}/certificate

%files
%dir %{_datadir}/ansible
%dir %{_datadir}/ansible/roles
%if 0%{?rolealtprefix:1}
%{_datadir}/ansible/roles/%{rolealtprefix}kdump
%{_datadir}/ansible/roles/%{rolealtprefix}postfix
%{_datadir}/ansible/roles/%{rolealtprefix}selinux
%{_datadir}/ansible/roles/%{rolealtprefix}timesync
%{_datadir}/ansible/roles/%{rolealtprefix}network
%{_datadir}/ansible/roles/%{rolealtprefix}storage
%{_datadir}/ansible/roles/%{rolealtprefix}metrics
%{_datadir}/ansible/roles/%{rolealtprefix}tlog
%{_datadir}/ansible/roles/%{rolealtprefix}kernel_settings
%{_datadir}/ansible/roles/%{rolealtprefix}logging
%{_datadir}/ansible/roles/%{rolealtprefix}nbde_server
%{_datadir}/ansible/roles/%{rolealtprefix}nbde_client
%{_datadir}/ansible/roles/%{rolealtprefix}certificate
%endif
%{_datadir}/ansible/roles/%{roleprefix}kdump
%{_datadir}/ansible/roles/%{roleprefix}postfix
%{_datadir}/ansible/roles/%{roleprefix}selinux
%{_datadir}/ansible/roles/%{roleprefix}timesync
%{_datadir}/ansible/roles/%{roleprefix}network
%{_datadir}/ansible/roles/%{roleprefix}storage
%{_datadir}/ansible/roles/%{roleprefix}metrics
%{_datadir}/ansible/roles/%{roleprefix}tlog
%{_datadir}/ansible/roles/%{roleprefix}kernel_settings
%{_datadir}/ansible/roles/%{roleprefix}logging
%{_datadir}/ansible/roles/%{roleprefix}nbde_server
%{_datadir}/ansible/roles/%{roleprefix}nbde_client
%{_datadir}/ansible/roles/%{roleprefix}certificate
%doc %{_pkgdocdir}/*/example-*-playbook.yml
%doc %{_pkgdocdir}/network/example-inventory
%doc %{_pkgdocdir}/*/README.md
%doc %{_pkgdocdir}/*/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}kdump/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}postfix/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}selinux/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}timesync/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}network/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}storage/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}metrics/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}tlog/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}kernel_settings/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}logging/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}nbde_server/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}nbde_client/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}certificate/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}kdump/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}postfix/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}selinux/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}timesync/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}network/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}storage/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}metrics/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}tlog/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}kernel_settings/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}logging/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}nbde_server/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}nbde_client/README.html
%doc %{_datadir}/ansible/roles/%{roleprefix}certificate/README.html


%license %{_pkgdocdir}/*/COPYING
%license %{_pkgdocdir}/*/LICENSE
%license %{_datadir}/ansible/roles/%{roleprefix}kdump/COPYING
%license %{_datadir}/ansible/roles/%{roleprefix}postfix/COPYING
%license %{_datadir}/ansible/roles/%{roleprefix}selinux/COPYING
%license %{_datadir}/ansible/roles/%{roleprefix}timesync/COPYING
%license %{_datadir}/ansible/roles/%{roleprefix}network/LICENSE
%license %{_datadir}/ansible/roles/%{roleprefix}storage/LICENSE
%license %{_datadir}/ansible/roles/%{roleprefix}metrics/LICENSE
%license %{_datadir}/ansible/roles/%{roleprefix}tlog/LICENSE
%license %{_datadir}/ansible/roles/%{roleprefix}kernel_settings/LICENSE
%license %{_datadir}/ansible/roles/%{roleprefix}kernel_settings/COPYING
%license %{_datadir}/ansible/roles/%{roleprefix}logging/LICENSE
%license %{_datadir}/ansible/roles/%{roleprefix}logging/COPYING
%license %{_datadir}/ansible/roles/%{roleprefix}nbde_server/LICENSE
%license %{_datadir}/ansible/roles/%{roleprefix}nbde_client/LICENSE
%license %{_datadir}/ansible/roles/%{roleprefix}certificate/LICENSE

%changelog
* Tue Sep 22 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-20
- storage: backport upstream PR #168 to prevent toggling encryption in safe mode,
  as it is a destructive operation. Resolves rhbz#1881524

* Mon Aug 24 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-19
- Rebase network role to latest upstream, resolves rhbz#1800627
  Drop a downstream patch with a test workaround that is not needed anymore.
- Fix script for role prefix transformation
- Rebase metrics role to pick up test changes, PR #19
- Rebase kernel_settings role to latest upstream, resolves rhbz#1851557

* Mon Aug 24 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-18
- Rebase storage role to latest upstream, resolves rhbz#1848254, rhbz#1851654,
  rhbz#1862867
- Rebase nbde_client role to latest upstream, resolves rhbz#1851654
- Rebase logging role to latest upstream, resolves rhbz#1851654, rhbz#1861318
- Rebase metrics role to latest upstream, resolves rhbz#1869390, rhbz#1869389,
  rhbz#1868378

* Fri Aug 21 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-17
- Rebase certificate role to latest upstream, resolves rhbz#1859547

* Mon Aug 10 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-16
- Rebase logging role to latest upstream, resolves rhbz#1854546, rhbz#1861318,
  rhbz#1860896, adds test for rhbz#1850790
- Rebase metrics role to latest upstream, resolves rhbz#1855544, rhbz#1855539,
  rhbz#1848763
- Fix whitespace in postfix role patch

* Fri Jul 31 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-15
- Rebase storage role to latest upstream, resolves rhbz#1854191, rhbz#1848250,
  rhbz#1850790 (including test)
- Rebase nbde_client role to latest upstream, adds test for rhbz#1850790
- Rebase certificate role to latest upstream, adds test for rhbz#1850790
- Rebase nbde_server role to latest upstream, resolves rhbz#1850790
  (including test)
- Rebase tlog role to latest upstream, resolves rhbz#1855424
- Rebase kernel_settings role to rev b8bc86b, resolves rhbz#1850790
- Add EL 8 to supported versions in postfix and kdump role metadata,
  resolves rhbz#1861661

* Mon Jul 20 2020 Rich Megginson <rmeggins@redhat.com> - 1.0-14
- Rebase certificate role to latest upstream, resolves rhbz#1858840

* Fri Jul 17 2020 Rich Megginson <rmeggins@redhat.com> - 1.0-13
- Rebase certificate role to latest upstream, resolves rhbz#1858316, rhbz#1848745

* Mon Jun 29 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-12
- Rebase network role to latest upstream, resolves rhbz#1822777, rhbz#1848472
- Rebase logging role to latest upstream, resolves rhbz#1850790,
  rhbz#1851804, rhbz#1848762
- Rebase certificate role to latest upstream, resolves rhbz#1848742,
  rhbz#1850790
- Rebase nbde_client role to latest upstream, resolves rhbz#1848766,
  rhbz#1850790

* Mon Jun 15 2020 Pavel Cahyna <pcahyna@redhat.com> - 1.0-11
- Rebase network role to latest upstream
- Remove all the soon-unnecessary tier1 tags in test
- Add a workaround for rhbz#1800627 in test
- Modify patches to remove tier1 tags
- Add metrics, tlog, logging, kernel_settings roles
- Add nbde_client, nbde_server, certificate roles
- Rebase storage role to latest upstream: adds support for mdraid, LUKS,
  swap manangement

* Mon Oct 21 2019 Pavel Cahyna <pcahyna@redhat.com> - 1.0-10
- Add the storage_safe_mode option, true by default, to prevent accidental
  data removal: rhbz#1763242, issue #42, PR #43 and #51.

* Thu Aug 15 2019 Pavel Cahyna <pcahyna@redhat.com> - 1.0-9
- Add the storage role

* Thu Jun 13 2019 Pavel Cahyna <pcahyna@redhat.com> - 1.0-7
- Update tests for the network role
- Fix typo in a test for the timesync role
- Tag tests suitable for Tier1 testing
- Rebase the network role to add support for device features (PR#115,
  rhbz#1696703) and atomic changes (PR#119, rhbz#1695161)
- network: apply upstream PR#121: allow modifying interface attributes
  without disrupting services (rhbz#1695157)

* Wed May 29 2019 Pavel Cahyna <pcahyna@redhat.com> - 1.0-6
- Rebase the selinux role, fixes typo in tests, uncovered by Ansible 2.7,
  (rhbz#1677743) and lists all input variables in defaults
  to make Satellite aware of them (rhbz#1674004, PR#43)
- Rebase the kdump role to fix check mode problems: rhbz#1685904
- Rebase the timesync role: fixes check mode problems (rhbz#1685904)
  and lists all input variables in defaults (rhbz#1674004)
- Rebase the network role: keeps the interface up for state: up
  if persistent_state is absent and solves problems with defining
  VLAN and MACVLAN interface types (issue #19) (rhbz#1685902)

* Sat Jan 12 2019 Pavel Cahyna <pcahyna@redhat.com> - 1.0-5
- spec file improvement: Unify the source macros with deftag() and defcommit()
- Update to upstream released versions and drop unnecessary patches.
- Unify the spec file with Fedora (no functional changes intended).
- Misc spec file comments fixes (by Mike DePaulo)
- Fix rpmlint error by escaping a previous changelog entry with a macro (by Mike DePaulo)
- Comply with Fedora guidelines by always using "cp -p" in %%install (by Mike DePaulo)
- Rebase network role - doc improvements, Fedora 29 and Ansible 2.7 support
- Regenerate network role patch to apply without offset
- Rebase kdump role to fix a forgotten edit, rhbz#1645633
- Update timesync examples: add var prefix (rhbz#1642152), correct role prefix
- Add Obsoletes for the -techpreview subpackage
- Add warnings to role READMEs and other doc updates, rhbz#1616018
- network: split the state setting into state and persistent_state, rhbz#1616014
- depend on python-jmespath as Ansible will not ship it, rhbz#1660559

* Tue Aug 14 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.0-4
- Format the READMEs as html, by vdolezal, with changes to use highlight
  (source-highlight does not understand YAML)

* Thu Aug  9 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.0-3
- Rebase the network role to the last revision (d866422).
  Many improvements to tests, introduces autodetection of the current provider
  and defaults to using profile name as interface name.
- Rebase the selinux, timesync and kdump roles to their 1.0rc1 versions.
  Many changes to the role interfaces to make them more consistent
  and conforming to Ansible best practices.
- Update the description.

* Fri May 11 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-4
- Fix complaints about /usr/bin/python during RPM build by making the affected scripts non-exec
- Fix merge botch

* Mon Mar 19 2018 Troy Dawson <tdawson@redhat.com> - 0.6-3.1
- Use -a (after cd) instead of -b (before cd) in %setup

* Wed Mar 14 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-3
- Minor corrections of the previous change by Till Maas.

* Fri Mar  9 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-2
- Document network role options: static routes, ethernet, dns
  Upstream PR#36, bz1550128, documents bz1487747 and bz1478576

* Tue Jan 30 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-1
- Drop hard dependency on ansible (#1525655), patch from Yaakov Selkowitz
- Update the network role to version 0.4, solves bz#1487747, bz#1478576

* Tue Dec 19 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-3
- kdump: fix the wrong conditional for ssh checking and improve test (PR#10)

* Tue Nov 07 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-2
- kdump: add ssh support. upstream PR#9, rhbz1478707

* Tue Oct 03 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-1
- SELinux: fix policy reload when SELinux is disabled on CentOS/RHEL 6
  (bz#1493574)
- network: update to b856c7481bf5274d419f71fb62029ea0044b3ec1 :
  makes the network role idempotent (bz#1476053) and fixes manual
  network provider selection (bz#1485074).

* Mon Aug 28 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.4-1
- network: update to b9b6f0a7969e400d8d6ba0ac97f69593aa1e8fa5:
  ensure that state:absent followed by state:up works (bz#1478910), and change
  the example IP adresses to the IANA-assigned ones.
- SELinux: fix the case when SELinux is disabled (bz#1479546).

* Tue Aug 8 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.3-2
- We can't change directories to symlinks (rpm bug #447156) so keep the old
  names and create the new names as symlinks.

* Tue Aug 8 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.3-1
- Change the prefix to linux-system-roles., keeping compatibility
  symlinks.
- Update the network role to dace7654feb7b5629ded0734c598e087c2713265:
  adds InfiniBand support and other fixes.
- Drop a patch included upstream.

* Mon Jun 26 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.2-2
- Leave a copy of README and COPYING in every role's directory, as suggested by T. Bowling.
- Move the network example inventory to the documentation directory together.
  with the example playbooks and delete the now empty "examples" directory.
- Use proper reserved (by RFC 7042) MAC addresses in the network examples.

* Tue Jun 6 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.2-1
- Update the networking role to version 0.2 (#1459203)
- Version every role and the package separately. They live in separate repos
  and upstream release tags are not coordinated.

* Mon May 22 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.1-2
- Prefix the roles in examples and documentation with rhel-system-roles.

* Thu May 18 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.1-1
- Update to 0.1 (first upstream release).
- Remove the tuned role, it is not ready yet.
- Move the example playbooks to /usr/share/doc/rhel-system-roles/$SUBSYSTEM
  directly to get rid of an extra directory.
- Depend on ansible.

* Thu May 4 2017  Pavel Cahyna <pcahyna@redhat.com> - 0-0.1.20170504
- Initial release.
- kdump r. fe8bb81966b60fa8979f3816a12b0c7120d71140
- postfix r. 43eec5668425d295dce3801216c19b1916df1f9b
- selinux r. 1e4a21f929455e5e76dda0b12867abaa63795ae7
- timesync r. 33a1a8c349de10d6281ed83d4c791e9177d7a141
- tuned r. 2e8bb068b9815bc84287e9b6dc6177295ffdf38b
- network r. 03ff040df78a14409a0d89eba1235b8f3e50a750


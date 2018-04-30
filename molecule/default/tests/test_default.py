import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_keepalived_is_installed(host):
    pkg = host.package('keepalived')
    assert pkg.is_installed


def test_keepalived_conf_file(host):
    f = host.file('/etc/keepalived/keepalived.conf')
    assert f.exists


def test_keepalived_running_and_enabled(host):
    svc = host.service('keepalived')
    assert svc.is_running
    assert svc.is_enabled

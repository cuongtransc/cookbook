"""
Fabfile template for python3
"""
# -*- coding: utf-8 -*-
from __future__ import print_function

from slackclient import SlackClient
from fabric.api import cd, env, task, run, settings, local
from fabfile_config import *
import traceback
from fabric.contrib.files import exists

LAST_CID_FILE = "last_commit_id.txt"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FabSlack(metaclass=Singleton):
    sc = SlackClient(SLACK_API_KEY)

    def send(self, **kargs):
        try:
            self.sc.api_call(
                "chat.postMessage",
                channel="#log-info",
                username='Deployment',
                # as_user=True,
                icon_emoji=":gear:",
                **kargs
            )
        except Exception:
            traceback.print_exc()


sc = FabSlack()


@task
def test(target_host):
    pass


@task
def set_host(target_host='dev'):
    """Set host before deploy,

    NOTE: plz configure ssh config file on your local machine first.
    Eg use: `fab set_host:dev deploy`
    :param: target_host string
    """
    env.use_ssh_config = True
    env.hosts = [target_host]


@task
def deploy():
    try:
        target_host = env.hosts[0]
    except IndexError:
        target_host = 'dev'

    with cd(HOST_API[target_host]['dir']):
        do_deploy()


def run_cmd(cmd, target_host=None, local_capture=True):
    """
    Run cmd base on local or remote host and return output or print output to terminal screen

    :param string cmd: Command to run
    :param string target_host: local or remote host name
    :param bool   local_capture: If true then return output and not print anything to terminal, if false then print output to terminal
    :return: Output string if capture=True or return nothing if capture=false
    """
    result = ''
    with settings(warn_only=True):
        fn = "local" if target_host == 'local' else "run"
        if fn == 'local':
            result = local(cmd, local_capture)  # Do not print to terminal and get the output
        else:
            result = run(cmd, warn_only=True, pty=False)
        if result.failed:
            print(result.stdout)
            attachments = [{
                "title": 'Command: {}'.format(result.command),
                "color": "danger",
                "pretext": 'Detail: {}'.format(result),
                "mrkdwn_in": ["text", "pretext"]
            }]
            sc.send(attachments=attachments, text="Deploy to *{}* error".format(env.hosts[0]))
            raise SystemExit()
        else:
            return result


def do_deploy():
    if not exists("{}/{}".format(HOST_API[env.hosts[0]]['dir'], LAST_CID_FILE)):
        save_last_commit()

    run_cmd("git pull")
    run_testing()
    restart_api()
    send_commit_applied()
    save_last_commit()


def run_testing():
    pass


def restart_api():
    pass


def get_current_commit():
    return run_cmd("git rev-parse HEAD")


def save_last_commit():
    run_cmd("git rev-parse HEAD > {}".format(LAST_CID_FILE))


def get_last_commit():
    return run_cmd("cat {}".format(LAST_CID_FILE))


def get_git_logs(last_commit_id, current_commit_id):
    return run_cmd("git log {}...{} --oneline --pretty=format:'%s'".format(last_commit_id, current_commit_id))


def send_commit_applied():
    last_commit_id = get_last_commit()
    current_commit_id = get_current_commit()
    commit_applied = get_git_logs(last_commit_id, current_commit_id)
    if commit_applied:
        commit_applied = "••• " + commit_applied
        commit_applied = commit_applied.replace("\n", "\n••• ")
    attachments = [
        {
            "color": "good",
            "title": "Commit applied:",
            "text": commit_applied,
        },
    ]
    sc.send(attachments=attachments, text="Deploy to *{}* success".format(env.hosts[0]))

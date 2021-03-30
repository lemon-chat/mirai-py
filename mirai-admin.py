import argparse
import os
import shutil
import json
import codecs

from mirai_main import run_bot


def create_config_file(path: str, account: str):
    data = {
        'account': account,
        'host': '',
        'auth_key': '',
        'autologin': False
    }
    with codecs.open(filename=path, mode='w', encoding='utf-8') as f:
        json.dump(data, fp=f, indent=4)


def parser_add_arg(args):
    bot_path = os.path.join(os.getcwd() + os.sep + 'bots', args.account)
    if os.path.exists(bot_path):
        print('{} already exists.'.format(args.account))
        return
    os.makedirs(bot_path)
    create_config_file(os.path.join(bot_path, 'config.json'), args.account)


def parser_delete_arg(args):
    bot_path = os.path.join(os.getcwd() + os.sep + 'bots', args.account)
    if os.path.exists(bot_path):
        shutil.rmtree(bot_path)


def parser_run_arg(args):
    bot_path = os.path.join(os.getcwd() + os.sep + 'bots', args.account)
    if not os.path.exists(bot_path):
        print('Not found account {}'.format(args.account))
        return
    config_file = os.path.join(bot_path, 'config.json')
    if not os.path.exists(config_file):
        create_config_file(config_file, args.account)
    with codecs.open(filename=config_file, mode='r', encoding='utf-8') as f:
        config = json.load(f)
        if not config['host'] or not config['auth_key']:
            print('Please config the `host` and `auth_key` in {}'.format(config_file))
            return
    run_bot(config['host'], config['auth_key'], config['account'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='mirai-admin action')

    parser_add = subparsers.add_parser('add', help='add a bot account')
    parser_add.add_argument('account', type=str, help='qq account')
    parser_add.set_defaults(func=parser_add_arg)

    parser_add = subparsers.add_parser('delete', help='delete a bot account')
    parser_add.add_argument('account', type=str, help='qq account')
    parser_add.set_defaults(func=parser_delete_arg)

    parser_run = subparsers.add_parser('run', help='Run the specified qq account, if not specify then run the autologin account')
    parser_run.add_argument('account', type=str, nargs='?', default='', help='qq account, if not specify then run the autologin account')
    parser_run.set_defaults(func=parser_run_arg)

    args = parser.parse_args()
    if len(args._get_kwargs()) > 0:
        args.func(args)
    else:
        parser.print_help()
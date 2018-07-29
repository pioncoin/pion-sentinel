import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from piond import PionDaemon
from pion_config import PionConfig


def test_piond():
    config_text = PionConfig.slurp_config_file(config.pion_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000009c77e1208a736b8289762416db2472b644e35fe8341104e1de218673a0d'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000006b4dac951b8df45f31c642dbfc9591e801bad467cedeb0e07498cbe2554'

    creds = PionConfig.get_rpc_creds(config_text, network)
    piond = PionDaemon(**creds)
    assert piond.rpc_command is not None

    assert hasattr(piond, 'rpc_connection')

    # Pion testnet block 0 hash == 000006b4dac951b8df45f31c642dbfc9591e801bad467cedeb0e07498cbe2554
    # test commands without arguments
    info = piond.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert piond.rpc_command('getblockhash', 0) == genesis_hash

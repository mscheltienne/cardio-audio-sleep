from configparser import ConfigParser
from pathlib import Path

from bsl.triggers import TriggerDef


def load_triggers():
    """
    Load triggers from triggers.ini into a TriggerDef instance.

    Returns
    -------
    tdef : TriggerDef
        Trigger definitiopn containing: sound, omission, sync_start, sync_stop,
        iso_start, iso_stop, async_start, async_stop, baseline_start and
        baseline_stop
    """
    directory = Path(__file__).parent
    tdef = TriggerDef(directory / 'triggers.ini')

    keys = (
        'sound',
        'omission',
        'sync_start',
        'sync_stop',
        'iso_start',
        'iso_stop',
        'async_start',
        'async_stop',
        'baseline_start',
        'baseline_stop'
        )
    for key in keys:
        if not hasattr(tdef, key):
            raise ValueError(
                f"Key '{key}' is missing from trigger definition.")

    return tdef


def load_config():
    """
    Load config from config.ini.

    Returns
    -------
    config : dict

    """
    directory = Path(__file__).parent
    config = ConfigParser(inline_comment_prefixes=('#', ';'))
    config.optionxform = str
    config.read(str(directory / 'config.ini'))

    keys = (
        'block',
        'baseline',
        'synchronous',
        'isochronous',
        'asynchronous'
        )
    for key in keys:
        if not config.has_section(key):
            raise ValueError(
                f"Key '{key}' is missing from configuration.")

    # Convert all to int
    block = {key: int(value)
             for key, value in dict(config['block']).items()}
    baseline = {key: int(value)
                for key, value in dict(config['baseline']).items()}
    synchronous = {key: int(value)
                   for key, value in dict(config['synchronous']).items()}
    isochronous = {key: int(value)
                   for key, value in dict(config['isochronous']).items()}
    asynchronous = {key: int(value)
                    for key, value in dict(config['asynchronous']).items()}

    # Check keys
    assert 'inter_block' in block
    assert 'duration' in baseline
    assert all(key in synchronous
               for key in ('n_stimuli', 'n_omissions', 'edge_perc'))
    assert all(key in isochronous
               for key in ('n_stimuli', 'n_omissions', 'edge_perc'))
    assert all(key in asynchronous
               for key in ('n_stimuli', 'n_omissions', 'edge_perc'))

    # Overwrite edge_perc with float
    synchronous['edge_perc'] = config['synchronous'].getfloat('edge_perc')
    isochronous['edge_perc'] = config['isochronous'].getfloat('edge_perc')
    asynchronous['edge_perc'] = config['asynchronous'].getfloat('edge_perc')

    config = {
        'block': block,
        'baseline': baseline,
        'sync': synchronous,
        'iso': isochronous,
        'async': asynchronous
        }

    return config
import numpy as np
from numpy.typing import ArrayLike, NDArray

from ._checks import _check_type


def generate_async_timings(
    sequence_timings: ArrayLike,
    perc: float = 10.0,
) -> NDArray[float]:
    """Generate timings for an asynchronous block from a synchronous block.

    Given the sequence of timings of a synchronous block, generate the sequence
    of timings for the future asynchronous block(s).
    The 10% top and bottom timings are removed and the asynchronous timing
    sequence is generated by randomizing the remaining synchornous
    inter-stimuli timings.

    Parameters
    ----------
    sequence_timings : list | tuple | array
        List of timings at which an R-peak occurred.
    perc : float
        Bottom and top percentage of timings removed.

    Returns
    -------
    sequence_timings : array
        List of timings at which a stimuli occurs for the asynchronous blocks.
        None is returned if the sequence could not be generated.
    """
    _check_type(
        sequence_timings, (list, tuple, np.ndarray), "sequence_timings"
    )
    _check_type(perc, ("numeric",), "perc")
    if perc < 0 or 50 <= perc:
        raise ValueError(
            "Argument 'perc' should represent a percentage "
            f"between 0 and 50. Provided '{perc}'% is not "
            "valid."
        )

    # remove bottom and top perc%
    n = len(sequence_timings)
    diff = np.diff(sequence_timings)
    mask = np.where(
        (np.percentile(diff, perc) <= diff)
        & (diff <= np.percentile(diff, 100 - perc))
    )
    assert diff[mask].size != 0

    # generate sequence of 'n-1' valid inter-stimulus delays
    delays = np.random.choice(diff[mask], size=n - 1, replace=True)
    timings = np.zeros((n,))
    for k, delay in enumerate(delays):
        timings[k + 1] = timings[k] + delay
    return timings

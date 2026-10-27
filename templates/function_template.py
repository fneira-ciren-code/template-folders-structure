"""function_name.py: one-sentence description of what this module provides."""


def function_name(x: object) -> object:
    """Short title of the function.

    Args:
        x: Description of `x` (type, units, CRS if spatial).

    Returns:
        Description of the returned object.

    Raises:
        ValueError: If `x` is None.
    """
    if x is None:
        raise ValueError("`x` must not be None.")

    return x

def get_width_height_from_args(resize_arg: str) -> list:
    """
    Args:
        resize_arg (str):

    Returns:

    """
    if not resize_arg:
        return None

    if len(resize_arg.split(",")) != 2:
        raise Exception(f"{resize_arg} is not a valid resize format. Use width,height: e.g. 800,600")

    for x in resize_arg.split(","):
        if not x:
            raise Exception(f"{resize_arg} is not a valid resize format. Use width,height: e.g. 800,600")

    return [int(x) for x in resize_arg.split(",")]

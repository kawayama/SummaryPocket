import logging


def setting_logger(logger):
    """ロガーの設定を行う

    Args:
        logger (_type_): ロガー
    """
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s %(levelname)8s %(module)15s %(message)s")

    try:
        handler = logging.FileHandler(filename="/proc/1/fd/1")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except (FileNotFoundError, PermissionError):
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

import atexit
import json
import logging.config
import logging.handlers
import pathlib

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    config_file = pathlib.Path("logger/config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def main() -> None:
    setup_logging()

    logger.debug("debug message", extra={"x": "hello"})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        1 / 0  # noqa
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()

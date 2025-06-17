import loguru as log
import pathlib as plib


log_info_path = plib.Path(__file__).parent / "log/log_info.log"
log_error_path = plib.Path(__file__).parent / "log/log_error.log"

# log.logger.remove()
log.logger.add(
    str(log_info_path),
    format="{time} {level} {message}",
    level="INFO",
    rotation="1 day",
)
log.logger.add(
    str(log_error_path),
    format="{time} {level} {message}",
    level="ERROR",
    rotation="1 day",
)
# log.logger.remove()


import logging
import os

log_dir = "EXP14_Output"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "app.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")

console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.debug("This is a DEBUG message - detailed information for debugging")
logger.info("This is an INFO message - general information about program flow")
logger.warning("This is a WARNING message - something unexpected happened")
logger.error("This is an ERROR message - a serious problem occurred")
logger.critical("This is a CRITICAL message - program may crash")

try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Exception caught - division by zero error")

print(f"\nLog file saved to: {log_file}")

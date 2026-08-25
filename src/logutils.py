from __future__ import annotations

import re
from logging import Logger, getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO
from pathlib import Path
from datetime import datetime, date as dtdate, time as dttime
from typing import TypedDict

__all__: list[str] = [
    'init',
    'load_logs',
    'clear_logs',
    'filter_logs',
    'tail_logs'
]

fmt: str = '%(asctime)s | %(filename)s:%(lineno)d | %(levelname)s | %(message)s'
datefmt: str = '%B %d, %Y | %I:%M:%S %p'


class LogEntry(TypedDict):
    date: str | dtdate
    time: str | dttime
    filename: str | Path
    line: int
    level: str
    message: str


type Logs = tuple[LogEntry, ...]

dflt_log_file = Path(r"D:\Python\python-project\logs\project.log")

LOG_PATTERN = re.compile(
    r'^(?P<date>.+?) \| (?P<time>.+?) \| '
    r'(?P<filename>.+?):(?P<line>\d+) \| '
    r'(?P<level>\w+) \| '
    r'(?P<message>.*)$'
)


def init(
        log_file: Path | str = dflt_log_file,
        mode: str = 'a'
) -> None:
    """
    Configure root logger with console and file output.

    - File logs: INFO+
    - Console logs: DEBUG+

    Parameters
    ----------
    log_file : Path | str
        Destination log file path.
    mode : str
        File open mode ('a', 'w', etc.)

    Raises
    ------
    TypeError
        If argument types are invalid.
    """
    if not isinstance(log_file, (str, Path)):
        raise TypeError("log_file must be Path or str")
    if not isinstance(mode, str):
        raise TypeError("mode must be str")

    logger: Logger = getLogger()
    logger.setLevel(DEBUG)

    file_handler = FileHandler(Path(log_file), mode=mode, encoding="utf-8")
    console_handler = StreamHandler()

    file_handler.setLevel(INFO)
    console_handler.setLevel(DEBUG)

    formatter = Formatter(fmt=fmt, datefmt=datefmt)

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def load_logs(
        log_file: Path | str = dflt_log_file,
        advanced: bool = False
) -> Logs:
    """
    Parse structured logs from a file.

    Expected format:
    date | time | filename:line | level | message

    Parameters
    ----------
    log_file : Path | str
        Path to log file.
    advanced : bool
        If True, converts:
        - date/time → datetime objects
        - filename → Path

    Returns
    -------
    Logs
        Parsed log entries.

    Raises
    ------
    FileNotFoundError
    TypeError
    """
    if not isinstance(log_file, (str, Path)):
        raise TypeError("log_file must be Path or str")
    if not isinstance(advanced, bool):
        raise TypeError("advanced must be bool")

    path = Path(log_file)
    if not path.exists():
        raise FileNotFoundError(path)

    logs: list[LogEntry] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        match_ = LOG_PATTERN.match(line)
        if not match_:
            continue

        date_part = match_["date"]
        time_part = match_["time"]
        filename = match_["filename"]
        lineno = int(match_["line"])
        level = match_["level"]
        message = match_["message"]

        if advanced:
            dt = datetime.strptime(f"{date_part} | {time_part}", datefmt)

            logs.append({
                "date": dt.date(),
                "time": dt.time(),
                "filename": Path(filename),
                "line": lineno,
                "level": level,
                "message": message
            })
        else:
            logs.append({
                "date": date_part,
                "time": time_part,
                "filename": filename,
                "line": lineno,
                "level": level,
                "message": message
            })

    return tuple(logs)


def clear_logs(log_file: Path | str = dflt_log_file) -> None:
    """
    Clear all contents of a log file.

    Parameters
    ----------
    log_file : Path | str
        Target log file.

    Raises
    ------
    FileNotFoundError
    TypeError
    """
    if not isinstance(log_file, (Path, str)):
        raise TypeError("log_file must be Path or str")

    path = Path(log_file)

    if not path.exists():
        raise FileNotFoundError(path)

    path.write_text("", encoding="utf-8")


def filter_logs(
        keyword: str,
        filter_by: str = "message",
        log_file: Path | str = dflt_log_file,
        advanced: bool = False
) -> Logs:
    """
    Filter logs by keyword in a selected field.

    Parameters
    ----------
    keyword : str
        Text to search for (case-insensitive).
    filter_by : str
        Field to search within.
    log_file : Path | str
        Source log file.
    advanced : bool
        If True, converts:
        - date/time → datetime objects
        - filename → Path

    Returns
    -------
    Logs
        Matching entries.

    Raises
    ------
    KeyError
    TypeError
    """
    if not isinstance(log_file, (Path, str)):
        raise TypeError("log_file must be Path or str")

    logs = load_logs(Path(log_file), advanced)

    if not logs:
        return ()

    if filter_by not in logs[0]:
        raise KeyError("filter_by must be a valid log field")

    return tuple(
        log for log in logs
        if keyword.lower() in str(log[filter_by]).lower()
    )


def tail_logs(
        n: int = 10,
        log_file: Path | str = dflt_log_file,
        advanced: bool = False
) -> Logs:
    """
    Return the last N log entries.

    Parameters
    ----------
    n : int
        Number of entries to return.
    log_file : Path | str
        Source log file.
    advanced : bool
        If True, converts:
        - date/time → datetime objects
        - filename → Path

    Returns
    -------
    Logs
        Last N log entries.

    Raises
    ------
    TypeError
    """
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if not isinstance(log_file, (Path, str)):
        raise TypeError("log_file must be Path or str")

    logs = load_logs(Path(log_file), advanced)
    return logs[-n:]

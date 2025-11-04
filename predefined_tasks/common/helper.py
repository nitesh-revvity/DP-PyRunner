from devicepilot.pylog.pylogger import PyLogger
from devicepilot.py_pli.pylib import send_msg
import json
from typing import TextIO

async def send_to_gc(msg: str = "", log = False, error = False, report: TextIO = None):
    """
    sends msg to gc output,
    if log: to logger.info,
    if log and error: logger.error
    if report: write msg also to report
    """
    print("============================================================================")
    print(f"send_to_gc: {msg}")
    print(f"log: {log}, error: {error}, report: {report}")


    content = {"result": msg}
    log_prefix = "gc_predefined_tasks> "
    if log and not error:
        PyLogger.logger.info(log_prefix + msg)
    elif log and error:
        PyLogger.logger.error(log_prefix + msg)
    if report:
        report.write(msg + "\n")
    await send_msg(json.dumps(content))
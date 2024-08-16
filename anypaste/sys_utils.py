import asyncio
from time import time
from logging import INFO, basicConfig, getLogger


class AsyncLoggingContextManager:
    '''
    Asynchronous Usage:
    -------------------
    # Basic async usage
    async with LoggingContextManager("Simple async code block"):
        await asyncio.sleep(1)
        print("Doing some async work...")

    # Async with time benchmarking
    async with LoggingContextManager("Benchmarking async code block", time_benchmark=True):
        await asyncio.sleep(1)  # Simulating some async work
        print("Doing some benchmarked async work...")

    # Handling exceptions in async context
    try:
        async with LoggingContextManager("Async block with potential error", time_benchmark=True):
            await asyncio.sleep(0.5)
            raise ValueError("Example async error")
    except ValueError:
        print("Caught the error outside the async context manager")

    Parameters:
    -----------
    message : str
        The message to log at the start and end of the context.
    time_benchmark : bool, optional
        If True, log the duration of the context execution (default is False).
    level : int, optional
        The logging level to use (default is logging.INFO).
    '''

    def __init__(self, message, time_benchmark=False, level=INFO):
        self.message = message
        self.time_benchmark = time_benchmark
        self.level = level
        self.logger = getLogger(__name__)

        if not getLogger().handlers:
            _log_format = '%(asctime)s - %(levelname)s - %(message)s'
            basicConfig(level=INFO, format=_log_format)

    async def __aenter__(self):
        await asyncio.to_thread(self.logger.log, self.level, f"Start: {self.message}")
        if self.time_benchmark:
            self.start_time = time()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.time_benchmark:
            duration = time() - self.start_time
            await asyncio.to_thread(
                self.logger.log,
                self.level,
                f"End: {self.message} (Duration: {duration:.4f} seconds)"
            )
        else:
            await asyncio.to_thread(self.logger.log, self.level, f"End: {self.message}")

        if exc_type:
            await asyncio.to_thread(
                self.logger.error,
                f"An error occurred: {exc_type.__name__}: {exc_value}"
            )

        return False  # Allow exceptions to propagate


async def asyncize(sync_func, *args):
    return await asyncio.get_event_loop().run_in_executor(None, sync_func, *args)

import asyncio
from pyperclip import copy as pycopy

# App modules:
from sys_utils import (
    AsyncLoggingContextManager, asyncize
)
from app_utils import accummulator
from constants import (
    PREFIX,
    SUFFIX,
    ENDING_STRING,
    LOGGER_TEXT,
)

# Empemeral Functions:
from funcs import adder, sql_repl, get_rms_id


async def main():
    # Empemeral Function INIT:
    # payload = {'current_sum': 0, 'previous_result': 0}
    payload = {}
    active_func = get_rms_id
    # Optional: 
    active_func = await accummulator(payload, active_func)

    try:
        while True:
            input_text = await asyncize(input, "\nEnter text: ")
            if input_text == ENDING_STRING:
                print(f'''
                    You've pressed the {ENDING_STRING=}.
                    Exiting...
                ''')
                break
            
            async with AsyncLoggingContextManager(LOGGER_TEXT, time_benchmark=True):
                updated_text = await active_func(expr=input_text)

            result = f"{PREFIX}{updated_text}{SUFFIX}"
            await asyncize(pycopy, result)
            print(f'''
                Pasted to Clipboard!
            ''')
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == '__main__':
    asyncio.run(main())

import rich

async def ask_to_run_command(command: str) -> None:
    console = rich.get_console()
    console.print('')
    console.print('Execute the following command in terminal and press enter:')
    console.print('')
    console.print(f'    {command}')
    console.print('')
    console.input('[Press enter]')

from typing import Callable, List, Optional

import aiogram
from aiogram.filters import Command

from app.bot_controller.decorators import skip_empty_command


class Router(aiogram.Router):
    """
    Custom router for command handlers. It allows to register command handlers with a decorator.
    """
    _all_routers: List = []

    def __init__(self, *, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.command_list: List[str] = []
        self._all_routers.append(self)

    @classmethod
    def get_all_commands(cls) -> List[str]:
        """Get all commands from all routers."""
        all_commands = []
        for router in cls._all_routers:
            all_commands.extend(router.command_list)
        return all_commands

    def register(
        self,
        command: Optional[str] = None,
        description: Optional[str] = None,
        skip_empty_messages: bool = False,
    ) -> Callable:
        """
        Register a command handler with optional description and empty message handling.
        
        Args:
            command (Optional[str]): The command to register (e.g. "start", "help"). 
                                   If None, registers as a general message handler.
            description (Optional[str]): Description of the command to show in help menu.
            skip_empty_messages (bool): If True, skips empty messages after the command.
        
        Returns:
            Callable: The decorated handler function.
            
        Usage:
        ```python
            @router.register(command="start", description="Start the bot")
            async def start_handler(message: types.Message):
                return "Hello!"
                
            @router.register()  # General message handler
            async def default_handler(message: types.Message):
                return "I don't understand"
        ```
        """
        def decorator(command_handler: Callable) -> Callable:
            if command is None:
                self.message()(command_handler)
                return command_handler

            command_filter = Command(command)
            handler = command_handler
            if skip_empty_messages:
                handler = skip_empty_command(command=command)(command_handler)

            self.message(command_filter)(handler)

            if description:
                self.command_list.append(f"/{command} - {description}")

            return handler

        return decorator
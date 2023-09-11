from .dispatcher import bot, dp
from .on_startup import on_startup
from .start import command_start_handler
from .admin_panel import admin_panel

__all__ = [
    "bot",
    "dp",
    "on_startup",
    "command_start_handler",
    "admin_panel",
]

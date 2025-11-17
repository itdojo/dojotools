from .getos import getos
from .rootcheck import check_root
from .shellcommands import run_shell_cmd
from .linuxcommands import (
    link_down,
    link_up,
    set_mode,
    set_channel,
    get_iface_mode,
    set_mac,
    add_route,
    check_service,
    start_service,
    enable_service,
    stop_service,
    disable_service,
    is_installed
)

__all__ = [
    "getos",
    "check_root",
    "run_shell_cmd",
    "link_down",
    "link_up",
    "set_mode",
    "set_channel",
    "get_iface_mode",
    "set_mac",
    "add_route",
    "check_service",
    "start_service",
    "enable_service",
    "stop_service",
    "disable_service",
    "is_installed"
]
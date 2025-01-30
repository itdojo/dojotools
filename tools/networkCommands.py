def link_down(iface):
    return f"ip link set dev {iface} down"

def link_up(iface):
    return f"ip link set dev {iface} up"

def set_mode(iface, mode):
    # need to check if iw is installed.
    return f"iw dev {iface} set type {mode}"

def set_channel(iface, channel):
    # need to check if iw is installed.
    return f"iw dev {iface} set channel {channel}"

def get_iface_mode(iface):
    # need to check if iw is installed.
    return f"iw {iface} info"

def set_mac(iface, mac):
    return f"ip link set dev {iface} address {mac}"

def add_route(dest_net, gw, netmask, interface):
    return f"ip route add {dest_net} via {gw} netmask {netmask} dev {interface}"

def check_service(service):
    return f"systemctl is-active --quiet {service}"

def start_service(service):
    return f"systemctl start {service}"

def enable_service(service):
    return f"systemctl enable {service}"

def stop_service(service):
    return f"systemctl stop {service}"

def disable_service(service):
    return f"systemctl disable {service}"

def is_installed(package):
    return f"dpkg -s {package}"

def is_installed(command):
    result = subprocess.run(["which", command], capture_output=True, text=True)
    return result.returncode == 0
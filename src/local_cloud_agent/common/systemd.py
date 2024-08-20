import subprocess


def reload_systemd() -> None:
    try:
        subprocess.run(['systemctl', 'daemon-reload'], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('Failed to reload systemd daemon: {}'.format(e))

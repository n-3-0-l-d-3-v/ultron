"""Run an Ultron analysis inside a locked-down, network-less Docker container.

The sample is mounted read-only; only the project directory is writable. The
container has no network, no capabilities, a read-only root filesystem and
resource limits, so a hostile binary/firmware cannot phone home or touch the host.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

IMAGE = "ultron-sandbox"


def build_run_command(sample: Path, project: Path, *, image: str = IMAGE, memory: str = "4g", cpus: str = "2") -> list[str]:
    sample = sample.resolve()
    project = project.resolve()
    return [
        "docker", "run", "--rm",
        "--network", "none",
        "--read-only", "--tmpfs", "/tmp:rw,size=1g",
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--pids-limit", "512", "--memory", memory, "--cpus", cpus,
        "-v", f"{sample}:/in/{sample.name}:ro",
        "-v", f"{project}:/work",
        image, "-P", "/work", "analyze", f"/in/{sample.name}",
    ]


def build_image_command(context: Path, image: str = IMAGE) -> list[str]:
    return ["docker", "build", "-f", str(context / "sandbox" / "Dockerfile"), "-t", image, str(context)]


def docker_available() -> bool:
    if not shutil.which("docker"):
        return False
    return subprocess.run(["docker", "info"], capture_output=True).returncode == 0

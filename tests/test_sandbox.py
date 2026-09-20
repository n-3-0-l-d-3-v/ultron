from pathlib import Path

from ultron import sandbox


def test_run_command_is_locked_down(tmp_path):
    s = tmp_path / "fw.bin"
    s.write_bytes(b"x")
    cmd = sandbox.build_run_command(s, tmp_path)
    joined = " ".join(cmd)
    assert cmd[cmd.index("--network") + 1] == "none"
    assert "--read-only" in cmd and "--cap-drop" in cmd and "no-new-privileges" in joined
    assert f"{s.resolve()}:/in/fw.bin:ro" in cmd
    assert cmd[-2:] == ["analyze", "/in/fw.bin"]


def test_build_command_points_at_dockerfile():
    cmd = sandbox.build_image_command(Path("/repo"))
    assert cmd[:2] == ["docker", "build"] and cmd[-1] == str(Path("/repo"))

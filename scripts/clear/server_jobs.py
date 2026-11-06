#!/usr/bin/env python3
"""Inspect Linux CPU usage and explicitly stop selected local process trees."""
import argparse
import os
from pathlib import Path
import pwd
import re
import signal
import sys
import time

PROJECT = Path(__file__).resolve().parents[2]
TICKS = os.sysconf("SC_CLK_TCK")
PAGE_SIZE = os.sysconf("SC_PAGE_SIZE")


def read_process(pid):
    try:
        path = Path("/proc") / str(pid)
        raw = (path / "stat").read_text()
        fields = raw[raw.rfind(")") + 2:].split()
        return {"pid": pid, "ppid": int(fields[1]), "start": int(fields[19]),
                "ticks": int(fields[11]) + int(fields[12]), "state": fields[0],
                "rss": int(fields[21]) * PAGE_SIZE, "uid": path.stat().st_uid,
                "name": raw[raw.find("(") + 1:raw.rfind(")")]}
    except (OSError, ValueError, IndexError):
        return None


def snapshot():
    result = {}
    for path in Path("/proc").iterdir():
        if path.name.isdigit():
            row = read_process(int(path.name))
            if row:
                result[row["pid"]] = row
    return result


def details(row):
    path = Path("/proc") / str(row["pid"])
    try:
        argv = (path / "cmdline").read_bytes().decode(errors="replace").replace("\0", " ").strip()
    except OSError:
        argv = row["name"]
    try:
        cwd = os.readlink(path / "cwd")
    except OSError:
        cwd = "<不可读取>"
    return argv or f"[{row['name']}]", cwd


def display(text):
    text = re.sub(r"sk-[A-Za-z0-9_-]+", "<redacted>", text)
    text = re.sub(r"(?i)((?:api[_-]?key|token|password|secret)\s*[=:]\s*)[^\s]+", r"\1<redacted>", text)
    return "".join(c if c.isprintable() else " " for c in text)


def cpu_counters(cpus):
    result = [0] * 8
    for line in Path("/proc/stat").read_text().splitlines():
        fields = line.split()
        if fields and fields[0].startswith("cpu") and fields[0][3:].isdigit() and int(fields[0][3:]) in cpus:
            result = [a + b for a, b in zip(result, map(int, fields[1:9]))]
    return result


def cgroup_resources():
    # cgroup v2: resolve this process's group, rather than assuming host totals
    # are resources allocated to the container. Missing/hidden data stays unknown.
    try:
        entry = next(line[3:] for line in Path('/proc/self/cgroup').read_text().splitlines() if line.startswith('0::'))
        group = Path('/sys/fs/cgroup') / entry.lstrip('/')
        stats = dict(line.split() for line in (group / 'cpu.stat').read_text().splitlines())
        quota, period = (group / 'cpu.max').read_text().split()
        memory_max = (group / 'memory.max').read_text().strip()
        return {'cpu_usec': int(stats['usage_usec']),
                'quota': None if quota == 'max' else int(quota) / int(period),
                'memory_current': int((group / 'memory.current').read_text()),
                'memory_max': None if memory_max == 'max' else int(memory_max)}
    except (OSError, ValueError, KeyError, StopIteration):
        return None


def status(args):
    cpus = os.sched_getaffinity(0)
    before_cpu, before = cpu_counters(cpus), snapshot()
    before_group = cgroup_resources()
    started = time.monotonic()
    time.sleep(args.interval)
    after_cpu, after = cpu_counters(cpus), snapshot()
    after_group = cgroup_resources()
    elapsed = time.monotonic() - started
    delta = [max(0, b - a) for a, b in zip(before_cpu, after_cpu)]
    total = sum(delta) or 1
    busy = 100 * (total - delta[3] - delta[4]) / total
    print(f"主机：{os.uname().nodename}    CPU 亲和性允许：{len(cpus)} 核    采样：{elapsed:.1f} 秒")
    print(f"CPU 使用率：{busy:.1f}%（约 {busy * len(cpus) / 100:.1f} 核）；I/O 等待：{100 * delta[4] / total:.1f}%")
    print("系统负载（1 / 5 / 15 分钟）：" + " / ".join(f"{x:.2f}" for x in os.getloadavg()))
    memory = {line.split(':')[0]: int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines()}
    print(f"可见内存：可用 {memory.get('MemAvailable', 0) / 1048576:.1f} / 总计 {memory['MemTotal'] / 1048576:.1f} GiB")
    if before_group and after_group:
        group_cores = max(0, after_group['cpu_usec'] - before_group['cpu_usec']) / 1e6 / elapsed
        quota = after_group['quota']
        limit = f"{quota:g} 核" if quota is not None else '本级未限额'
        memory_limit = f"{after_group['memory_max'] / 2**30:.1f} GiB" if after_group['memory_max'] is not None else '本级未限额'
        print(f"当前 cgroup：CPU 使用约 {group_cores:.1f} 核 / 配额 {limit}；内存使用 {after_group['memory_current'] / 2**30:.1f} GiB / 上限 {memory_limit}")
    print("说明：负载不是 CPU 百分比；CPU/内存可见值不等于容器或调度器分配额度。")
    if not after_group:
        print("当前 cgroup 配额不可读取；请另查容器/调度器的资源分配。")
    rows = []
    for pid, row in after.items():
        previous = before.get(pid)
        row["cpu"] = None
        if previous and previous["start"] == row["start"]:
            row["cpu"] = max(0, row["ticks"] - previous["ticks"]) / TICKS / elapsed * 100
        argv, cwd = details(row)
        if args.project_only and not (cwd == str(PROJECT) or cwd.startswith(str(PROJECT) + '/') or str(PROJECT) + '/' in argv):
            continue
        row.update(argv=argv, cwd=cwd)
        rows.append(row)
    rows.sort(key=lambda r: (r["cpu"] or 0, r["rss"]), reverse=True)
    print("\n PID      PPID     用户          CPU%     内存MiB  状态  命令")
    for row in rows[:args.top]:
        try:
            user = pwd.getpwuid(row['uid']).pw_name
        except KeyError:
            user = str(row['uid'])
        cpu = "new" if row["cpu"] is None else f"{row['cpu']:.1f}"
        print(f"{row['pid']:7} {row['ppid']:8} {user[:12]:12} {cpu:>8} {row['rss']/1048576:11.1f}  {row['state']:2}  {display(row['argv'])[:180]}")
        if args.paths:
            print("  cwd: " + display(row['cwd']))
    print("\n进程 CPU%=100 表示约占用 1 核；多线程进程可以超过 100%。new 表示采样期间新出现。")
    return 0


def descendants(rows, roots):
    selected = set(roots)
    while True:
        expanded = selected | {pid for pid, row in rows.items() if row["ppid"] in selected}
        if expanded == selected:
            return selected
        selected = expanded


def protected_pids(rows):
    protected = {1, 2}
    pid = os.getpid()
    while pid > 0 and pid not in protected:
        protected.add(pid)
        pid = rows.get(pid, {}).get("ppid", 0)
    return protected


def alive(row):
    current = read_process(row["pid"])
    return bool(current and current["start"] == row["start"] and current["state"] not in {"Z", "X"})


def send_signal(row, sig):
    # A pidfd binds the signal to the original process even if the PID is reused.
    fd = None
    try:
        fd = os.pidfd_open(row["pid"])
        if alive(row):
            signal.pidfd_send_signal(fd, sig)
            print(f"{sig.name} -> PID {row['pid']} ({display(row['name'])})", flush=True)
    except ProcessLookupError:
        pass
    finally:
        if fd is not None:
            os.close(fd)


def stop(args):
    rows = snapshot()
    for pid in args.pid:
        if pid not in rows:
            raise ValueError(f"PID {pid} 不存在或不可读取；没有终止任何进程。")
    selected = descendants(rows, args.pid)
    protected = protected_pids(rows)
    if selected & protected:
        raise ValueError(f"拒绝终止系统初始进程、脚本自身或当前终端祖先进程：{sorted(selected & protected)}")
    targets = {pid: rows[pid] for pid in selected}
    if any(row["uid"] != os.geteuid() for row in targets.values()):
        raise ValueError("目标包含其他用户的进程；请使用作业所属账号运行。")
    print(f"目标：{len(targets)} 个进程（指定 PID 及其当前子孙进程），主机 {os.uname().nodename}")
    for row in sorted(targets.values(), key=lambda r: r['pid']):
        argv, cwd = details(row)
        print(f"PID {row['pid']} PPID {row['ppid']} {display(argv)[:180]}\n  cwd: {display(cwd)}")
    if not args.yes:
        print("\n仅预览，未终止任何进程。确认目标后追加 --yes；追加 --force 会在等待后强制杀死残留进程。")
        return 0
    if not hasattr(os, 'pidfd_open') or not hasattr(signal, 'pidfd_send_signal'):
        raise ValueError("终止功能需要 Linux pidfd 和 Python >=3.9；当前环境不支持，未发送信号。")
    # Validate access to all initial targets before sending the first signal.
    for row in targets.values():
        try:
            fd = os.pidfd_open(row['pid'])
        except ProcessLookupError:
            continue
        os.close(fd)
    for row in targets.values():
        send_signal(row, signal.SIGTERM)
    deadline = time.monotonic() + args.grace
    while True:
        rows = snapshot()
        active = {pid for pid, row in targets.items() if alive(row)}
        for pid in descendants(rows, active) - targets.keys():
            row = rows[pid]
            if pid in protected or row['uid'] != os.geteuid():
                continue
            targets[pid] = row
            send_signal(row, signal.SIGTERM)
        remaining = [row for row in targets.values() if alive(row)]
        if not remaining or time.monotonic() >= deadline:
            break
        time.sleep(0.2)
    if remaining and args.force:
        for row in remaining:
            send_signal(row, signal.SIGKILL)
        deadline = time.monotonic() + 3
        while any(alive(row) for row in remaining) and time.monotonic() < deadline:
            time.sleep(0.1)
    remaining = [row['pid'] for row in targets.values() if alive(row)]
    if remaining:
        print(f"仍存活的 PID：{remaining}。--force 可升级为 SIGKILL；D 状态进程可能须等待内核 I/O 返回。", file=sys.stderr)
        return 1
    print("选中的进程已停止。结果文件未删除；请重新执行 status 检查独立进程或上层管理器重启的作业。")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, epilog="仅管理当前节点可见进程。不会删除结果或取消调度器上的远程作业。")
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("status", help="采样 CPU、内存和占用最高的进程（只读）")
    inspect.add_argument("--interval", type=float, default=1.0, help="采样间隔秒数，默认 1")
    inspect.add_argument("--top", type=int, default=20, help="显示进程数，默认 20")
    inspect.add_argument("--project-only", action="store_true", help="按工作目录/命令路径筛选本项目进程；可能漏掉不携带项目路径的子进程")
    inspect.add_argument("--paths", action="store_true", help="显示进程工作目录，便于定位评估任务")
    kill = sub.add_parser("stop", help="预览或终止指定 PID 及其子孙进程")
    kill.add_argument("--pid", type=int, nargs="+", required=True, help="一个或多个本地作业主进程 PID")
    kill.add_argument("--yes", action="store_true", help="实际执行；省略时仅预览")
    kill.add_argument("--force", action="store_true", help="先 SIGTERM，等待 grace 秒后对残留进程发送 SIGKILL")
    kill.add_argument("--grace", type=float, default=10.0, help="正常终止等待秒数，默认 10；0 可立即升级")
    args = parser.parse_args(argv if argv is not None else (sys.argv[1:] or ["status"]))
    if args.command == "status" and (not 0.1 <= args.interval <= 60 or args.top < 1):
        parser.error("interval 必须在 0.1..60 秒之间，top 必须 >=1")
    if args.command == "stop" and (not 0 <= args.grace <= 300 or any(pid <= 0 for pid in args.pid)):
        parser.error("grace 必须在 0..300 秒之间，PID 必须为正数")
    try:
        return status(args) if args.command == "status" else stop(args)
    except (OSError, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

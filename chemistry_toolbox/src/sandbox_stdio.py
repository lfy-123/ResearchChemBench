"""Authenticated byte relay for external harnesses that require stdio MCP."""
import os
import json
import secrets
import selectors
import signal
import socket
import socketserver
import subprocess
import sys
import threading


def copy_streams(connection, source, destination):
    with selectors.DefaultSelector() as selector:
        selector.register(connection, selectors.EVENT_READ)
        selector.register(source, selectors.EVENT_READ)
        while True:
            for key, _ in selector.select():
                data = os.read(key.fd, 65536)
                if not data:
                    return 'peer_closed' if key.fileobj is connection else 'stdio_closed'
                if key.fileobj is connection:
                    destination.write(data); destination.flush()
                else:
                    connection.sendall(data)


def serve(spec, token, workspace, log_path):
    children = []
    class Handler(socketserver.StreamRequestHandler):
        rbufsize = 0
        def handle(self):
            header = json.loads(self.rfile.readline(512))
            if not secrets.compare_digest(header.get('token', ''), token):
                return
            with open(log_path, 'ab') as log:
                child = subprocess.Popen(spec['command'], cwd=workspace, env={**os.environ, **spec['environment'],
                    'RESEARCHCHEMBENCH_TOOL_CALLER': 'adapter' if header.get('caller') == 'adapter' else 'client'},
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log, start_new_session=True)
            children.append(child)
            try:
                reason = copy_streams(self.connection, child.stdout, child.stdin)
                with open(log_path, 'a') as log:
                    log.write(f'MCP relay ended: {reason}; server_exit={child.poll()}\n')
            finally:
                if child.poll() is None:
                    os.killpg(child.pid, signal.SIGTERM)
                    try:
                        child.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(child.pid, signal.SIGKILL); child.wait()
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, children


if __name__ == '__main__':
    host, port = os.environ['RCB_MCP_ENDPOINT_' + sys.argv[1]].rsplit(':', 1)
    with socket.create_connection((host, int(port))) as connection:
        connection.sendall((json.dumps({'token': os.environ['RCB_MCP_AUTH_TOKEN'],
            'caller': os.environ.get('RESEARCHCHEMBENCH_TOOL_CALLER', 'client')}) + '\n').encode())
        copy_streams(connection, sys.stdin.buffer, sys.stdout.buffer)

#!/usr/bin/python
# AUTHOR : Isaac Palmersheim (TheEngineerGuy404)
# DATE : 2024-11-24
import socket
import select
import queue

HOST = ("0.0.0.0", 6969)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(0)
    server.bind(HOST)
    server.listen()

    streams = {
        server: None
    }

    while True:
        sockets = list(streams.keys())
        read, write, error = select.select(sockets, sockets[1:], sockets)

        for sock in read:
            if sock is server:
                conn, addr = sock.accept()

                for peer in sockets[1:]:
                    if peer is sock: continue
                    streams[peer].put(
                        f"[SERVER] {addr[0]} has joined the server!\n".encode()
                    )

                conn.setblocking(0)
                streams[conn] = queue.Queue()
                continue

            if payload := sock.recv(1024):
                payload = bytes(
                    list(
                        filter(
                            lambda x: int(x) < 128,
                            list(payload)
                        )
                    )
                )

                payload = payload.decode(encoding="ascii")
                for peer in sockets[1:]:
                    if peer is sock: continue
                    streams[peer].put(
                        f"[{peer.getpeername()[0]}] : {payload}".encode()
                    )
                continue

            del streams[sock]
            for peer in sockets[1:]:
                if peer is sock: continue
                streams[peer].put(
                    f"[SERVER] {sock.getpeername()[0]} has left the server!\n".encode()
                )
            sock.close()

        for sock in write:
            if not streams[sock].empty():
                sock.send(
                    streams[sock].get_nowait()
                )

        for sock in error:
            for peer in sockets[1:]:
                if peer is sock: continue
                streams[peer].put(
                    f"[SERVER] {sock.getpeername()[0]} has crashed and left the server!\n".encode()
                )

if __name__ == "__main__": main()
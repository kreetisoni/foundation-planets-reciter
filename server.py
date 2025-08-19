import asyncio

clients = set()  # keep track of connected clients

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[+] Connected with {addr}")
    clients.add(writer)

    try:
        while True:
            data = await reader.read(100)  # read up to 100 bytes
            if not data:  # client disconnected
                break

            message = data.decode().strip()
            print(f"[{addr}] {message}")

            # broadcast message to all clients
            for client in clients:
                if client != writer:  # don’t send back to sender
                    client.write(f"{addr}: {message}\n".encode())
                    await client.drain()
    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        print(f"[-] Disconnected {addr}")
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Server started on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())

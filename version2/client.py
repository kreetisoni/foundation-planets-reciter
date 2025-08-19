import asyncio

async def tcp_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    async def listen():
        while True:
            data = await reader.readline()
            if not data:
                break
            print(data.decode().strip())

    asyncio.create_task(listen())

    while True:
        msg = input("> ")
        writer.write((msg + "\n").encode())
        await writer.drain()

asyncio.run(tcp_client())

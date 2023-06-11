import asyncio
from pyjoystick.sdl2_async import Key, Joystick, run_event_loop


if __name__ == '__main__':
    import time
    from typing import Union
    import argparse

    devices = Joystick.get_joysticks()
    print("Devices:", devices)

    monitor = devices[0]
    monitor_keytypes = [Key.AXIS]


    clients = []
    loop = asyncio.get_event_loop()

    async def send(msg: Union[str, bytes], newline=''):
        str_msg = msg
        if isinstance(msg, str):
            msg = msg.encode()
        else:
            str_msg = msg.decode()

        cs = [c for c in clients]
        for client in cs:
            client.write(msg)
            # await client.drain()
        await asyncio.gather(*(client.drain() for client in cs), loop=loop)
        print('\r', str_msg, end=newline, flush=True)


    async def print_add(joy):
        await send('ADD: ' + str(joy), newline='\n')


    async def print_remove(joy):
        await send('REMOVE: ' + str(joy), newline='\n')


    async def key_received(key):
        if monitor is None:
            print(key, '==', key.value)
        elif key.joystick == monitor:
            print(key.joystick)
            #await send('EVENT: ' + str(key))
            monitor.update_key(key)

            #keys = '\t'.join((format_key(k) for k in monitor.keys if k.keytype in monitor_keytypes))
            #print('\r', keys, end='', flush=True)
            await send('EVENT: ' + str(key.value))
          


    

    async def add_client(reader, writer):
        clients.append(writer)

    async def run_server():
        server = await asyncio.start_server(add_client, '127.0.0.1', 8898)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

    async def main():
        await asyncio.gather(run_server(),
                             run_event_loop(print_add, print_remove, key_received))

    # Run the event loop
    loop.run_until_complete(main())

    for client in clients:
        print('Close the connection')
        client.close()
        loop.run_until_complete(client.wait_closed())
    loop.close()
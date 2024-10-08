import asyncio
import websockets
import json

connected_clients = set()

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f'Received message: {message}')
            data = json.loads(message)

            #データを送ったクライアントも含めて返す場合
            await asyncio.wait([client.send(json.dumps(data)) for client in connected_clients])

            #データを送ってきたクライアントには返さない場合
            # other_clients = connected_clients - {websocket} 
            # await asyncio.wait([client.send(json.dumps(data)) for client in other_clients])

    except websockets.exceptions.ConnectionClosed:
        print('Connection closed')
    finally:
        connected_clients.remove(websocket)

async def start_server():
    server = await websockets.serve(handle_client, '172.16.4.31', 8765)

asyncio.get_event_loop().run_until_complete(start_server())
asyncio.get_event_loop().run_forever()
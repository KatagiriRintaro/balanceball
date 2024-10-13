import asyncio
import websockets
import json
from datetime import datetime
from count import Count

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

connected_clients_server1 = set()
connected_clients_server2 = set()

players_list = []
start_list = {}

def default_converter(o):
                if isinstance(o, datetime):
                    # "T" なしでフォーマットする
                    return o.strftime("%Y-%m-%d %H:%M:%S.%f")


async def handle_client_server1(websocket, path):
    connected_clients_server1.add(websocket)
    try:
        async for message in websocket:

            data = json.loads(message)

            if data[:5] == 'Start':
                udid = data[5:]
                start_list[f"{udid}"] = "Start"
                are_all_values_same = len(set(start_list.values())) == 1
                if are_all_values_same:
                    send_tasks = [asyncio.create_task(client.send(json.dumps('GameStart'))) for client in connected_clients_server1]
                    await asyncio.wait(send_tasks)

            else:
                players_list.append(data)
                start_list[f"{data}"] = 0

                if len(players_list) == 2:

                    #データを送ったクライアントも含めて返す場合
                    # 各クライアントにデータを送信するためのタスクを明示的に作成
                    send_tasks = [asyncio.create_task(client.send(json.dumps(f'Setting OK{udid}'))) for client in connected_clients_server1]
                    await asyncio.wait(send_tasks)
                
                else:
                    send_tasks = [asyncio.create_task(client.send(json.dumps(f'Setting Not Yet{udid}'))) for client in connected_clients_server1]
                    await asyncio.wait(send_tasks)

    except websockets.exceptions.ConnectionClosed:
        print('Connection closed')
    finally:
        connected_clients_server1.remove(websocket)

async def handle_client_server2(websocket, path):
    connected_clients_server2.add(websocket)
    try:
        async for message in websocket:

            data = json.loads(message)

            udid = data.get("udid")
            mag_data = data.get("data")

            TimeStamps = Count(mag_data, low_cut=1 ,high_cut=8, height=20, distance=20)

            response_data = {"udid" : udid, "TimeStamps" : TimeStamps}

            #データを送ったクライアントも含めて返す場合
            # 各クライアントにデータを送信するためのタスクを明示的に作成
            # send_tasks = [asyncio.create_task(client.send(json.dumps(TimeStamps, default=default_converter))) for client in connected_clients]
            # await asyncio.wait(send_tasks)


            #データを送ってきたクライアントには返さない場合
            other_clients = connected_clients_server2 - {websocket} 
            await asyncio.wait([client.send(json.dumps(response_data, default=default_converter)) for client in other_clients])

    except websockets.exceptions.ConnectionClosed:
        print('Connection closed')
    finally:
        connected_clients_server2.remove(websocket)

async def start_server1():
    print("Starting WebSocket server1...")  # サーバー起動時のログ
    server = await websockets.serve(handle_client_server1, '172.16.4.31', 8764)
    print("WebSocket server1 started!")  # サーバー起動後のログ
    await server.wait_closed()

async def start_server2():
    print("Starting WebSocket server2...")  # サーバー起動時のログ
    server = await websockets.serve(handle_client_server2, '172.16.4.31', 8765)
    print("WebSocket server2 started!")  # サーバー起動後のログ
    await server.wait_closed()

async def start_servers():
    await asyncio.gather(
        start_server1(),start_server2()
    )

asyncio.run(start_servers())  # サーバの起動
using System;
using UnityEngine;
using WebSocketSharp;  // WebSocketSharpライブラリを使用

public class MainController : MonoBehaviour
{
    private WebSocket ws;

    void Start()
    {
        Debug.Log("Startメソッドが実行されました。");
        // WebSocketの初期化
        ws = new WebSocket("ws://172.16.4.31:8765/");

        // 接続のオープン
        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("WebSocket接続が確立されました。");
        };

        // メッセージ受信時のイベント
        ws.OnMessage += (sender, e) =>
        {
            Debug.Log("サーバーからのメッセージ: " + e.Data);
        };

        // エラー発生時のイベント
        ws.OnError += (sender, e) =>
        {
            Debug.LogError("エラーが発生しました: " + e.Message);
        };

        // 接続クローズ時のイベント
        ws.OnClose += (sender, e) =>
        {
            Debug.Log("WebSocket接続が閉じられました。");
        };

        // WebSocketに接続
        ws.Connect();
    }

    void OnDestroy()
    {
        // WebSocket接続を閉じる
        if (ws != null && ws.IsAlive)
        {
            ws.Close();
            Debug.Log("WebSocket接続を閉じました。");
        }
    }

    void Update()
    {
        // 必要ならここでデータ送信などを行う
        if (Input.GetKeyDown(KeyCode.Space))
        {
            ws.Send("Hello from Unity!");
            Debug.Log("メッセージを送信しました。");
        }
    }
}

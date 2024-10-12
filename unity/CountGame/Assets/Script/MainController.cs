using System;
using UnityEngine;
using WebSocketSharp;  // WebSocketSharpライブラリを使用
using System.Collections.Generic;
using System.Linq;
using System.Globalization;

public class MainController : MonoBehaviour
{
    private List<DateTime> preTimeStamps;
    private List<DateTime> postTimeStamps;
    private int Count = 0;
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

            if (Count == 0)
            {
                postTimeStamps = ParseStringToDynamicList(e.Data);
                // postTimeStampsリストを文字列に変換してログに出力
                string postTimeStampsString = string.Join(", ", postTimeStamps.Select(ts => ts.ToString("yyyy-MM-dd HH:mm:ss.fff")));
                Debug.Log("postTimeStamps: " + postTimeStampsString);

                Count = 1;
            }

            else
            {
                preTimeStamps = DeepCopyDynamicList(postTimeStamps);
                postTimeStamps = ParseStringToDynamicList(e.Data);
                // postTimeStampsリストを文字列に変換してログに出力
                string preTimeStampsString = string.Join(", ", preTimeStamps.Select(ts => ts.ToString("yyyy-MM-dd HH:mm:ss.fff")));
                Debug.Log("preTimeStamps: " + preTimeStampsString);
                // postTimeStampsリストを文字列に変換してログに出力
                string postTimeStampsString = string.Join(", ", postTimeStamps.Select(ts => ts.ToString("yyyy-MM-dd HH:mm:ss.fff")));
                Debug.Log("postTimeStamps: " + postTimeStampsString);
            }
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

    List<DateTime> ParseStringToDynamicList(string data)
    {
        data = data.Trim('[', ']');  // JSON配列の[]を除去
        string[] items = data.Split(',');  // カンマで区切る
        List<DateTime> result = new List<DateTime>();

        foreach (string item in items)
        {
            string trimmedItem = item.Trim().Trim('"');  // 余分なスペースと " を除去

            // 6桁のマイクロ秒が含まれている場合、3桁に切り詰める
            int dotIndex = trimmedItem.LastIndexOf('.');
            if (dotIndex != -1 && trimmedItem.Length - dotIndex - 1 > 3)
            {
                // 3桁まで残して切り詰める
                trimmedItem = trimmedItem.Substring(0, dotIndex + 4);  // 小数点+3桁
            }

            // パース処理
            if (DateTime.TryParseExact(trimmedItem, "yyyy-MM-dd HH:mm:ss.fff", CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime parsedDate))
            {
                result.Add(parsedDate);
            }
            else
            {
                Debug.LogWarning($"無効な日時フォーマット: {trimmedItem}");
            }
        }
        return result;
    }



    List<DateTime> DeepCopyDynamicList(List<DateTime> source)
    {
        return new List<DateTime>(source);
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

    }
}

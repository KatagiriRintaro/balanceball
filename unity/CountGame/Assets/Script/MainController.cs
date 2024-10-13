using System;
using UnityEngine;
using WebSocketSharp;  // WebSocketSharpライブラリを使用
using System.Collections.Generic;
using System.Linq;
using System.Globalization;
using Newtonsoft.Json.Linq;

public class MainController : MonoBehaviour
{
    private List<DateTime> preTimeStamps;
    private List<DateTime> postTimeStamps;
    private List<Dictionary<int, string>> playerList;
    private int sendCount = 0;
    private int Count = 0;
    private bool shouldUpdateCount = false;
    private WebSocket wsRegister;
    private WebSocket wsForDataSend;
    public CounterController counterController1;
    public CounterController counterController2;

    void Start()
    {
        Debug.Log("Startメソッドが実行されました。");
        // WebSocketの初期化
        wsForDataSend = new WebSocket("ws://172.16.4.31:8765/");
        wsRegister = new WebSocket("ws://172.16.4.31:8764/");

        wsRegister.OnOpen += (sender, e) =>
        {
            Debug.Log("WebSocket1接続が確立されました。");
        };

        // 接続のオープン
        wsForDataSend.OnOpen += (sender, e) =>
        {
            Debug.Log("WebSocket2接続が確立されました。");
        };

        wsRegister.OnMessage += (sender, e) =>
        {
            Debug.Log("サーバーからのメッセージ: " + e.Data);

            try
            {
                string modifiedData = "";

                if (e.Data.Contains("Setting OK"))
                {
                    modifiedData = e.Data.Replace("Setting OK", "");
                }

                else if (e.Data.Contains("Setting Not Yet"))
                {
                    modifiedData = e.Data.Replace("Setting Not Yet", "");
                }

                Dictionary<int, string> playerData = new Dictionary<int, string>();  // 辞書を作成


                if (playerList.Count == 0)
                {
                    playerData.Add(1, modifiedData);
                    playerList.Add(playerData);
                }
                else if (playerList.Count == 1)
                {
                    playerData.Add(2, modifiedData);
                    playerList.Add(playerData);
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"OnMessageで例外が発生しました: {ex.Message}\n{ex.StackTrace}");
            }
        };

        // メッセージ受信時のイベント
        wsForDataSend.OnMessage += (sender, e) =>
        {
            Debug.Log("サーバーからのメッセージ: " + e.Data);

            try
            {
                if (sendCount == 0)
                {
                    postTimeStamps = ParseStringToDynamicList(e.Data);
                    string postTimeStampsString = string.Join(", ", postTimeStamps.Select(ts => ts.ToString("yyyy-MM-dd HH:mm:ss.fff")));
                    Debug.Log("postTimeStamps: " + postTimeStampsString);

                    Count += postTimeStamps.Count;
                    Debug.Log("Count: " + Count);

                    shouldUpdateCount = true;

                    sendCount = 1;
                }
                else
                {
                    preTimeStamps = DeepCopyDynamicList(postTimeStamps);
                    postTimeStamps = ParseStringToDynamicList(e.Data);
                    string preTimeStampsString = string.Join(", ", preTimeStamps.Select(ts => ts.ToString("yyyy-MM-dd HH:mm:ss.fff")));
                    Debug.Log("preTimeStamps: " + preTimeStampsString);
                    string postTimeStampsString = string.Join(", ", postTimeStamps.Select(ts => ts.ToString("yyyy-MM-dd HH:mm:ss.fff")));
                    Debug.Log("postTimeStamps: " + postTimeStampsString);

                    CompareTimestamps();
                    Debug.Log("Count: " + Count);

                    shouldUpdateCount = true;
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"OnMessageで例外が発生しました: {ex.Message}\n{ex.StackTrace}");
            }
        };

        wsRegister.OnError += (sender, e) =>
        {
            Debug.LogError("Registerでエラーが発生しました: " + e.Message);
        };


        // エラー発生時のイベント
        wsForDataSend.OnError += (sender, e) =>
        {
            Debug.LogError("SendDataでエラーが発生しました: " + e.Message);
        };

        // 接続クローズ時のイベント
        wsRegister.OnClose += (sender, e) =>
        {
            Debug.Log("WebSocket接続が閉じられました。");
        };

        // 接続クローズ時のイベント
        wsForDataSend.OnClose += (sender, e) =>
        {
            Debug.Log("WebSocket接続が閉じられました。");
        };

        // WebSocketに接続
        wsRegister.Connect();
        wsForDataSend.Connect();
    }

    List<DateTime> ParseStringToDynamicList(string data)
    {
        List<DateTime> result = new List<DateTime>();

        try
        {
            // JSONを解析してTimeStampsを取得
            JObject jsonData = JObject.Parse(data);
            JArray timeStampsArray = (JArray)jsonData["TimeStamps"];  // TimeStamps配列を取得

            // TimeStampsをDateTimeのリストに変換
            foreach (string item in timeStampsArray)
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
        }
        catch (Exception ex)
        {
            Debug.LogError($"JSON解析に失敗しました: {ex.Message}");
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
        if (wsRegister != null && wsRegister.IsAlive && wsForDataSend != null && wsForDataSend.IsAlive)
        {
            wsRegister.Close();
            wsForDataSend.Close();
            Debug.Log("WebSocket接続を閉じました。");
        }
    }

    void CompareTimestamps()
    {
        // postTimeStamps と preTimeStamps の共通要素を取得
        var commonTimestamps = preTimeStamps.Intersect(postTimeStamps).ToList();

        // 共通部分のログ出力
        if (commonTimestamps.Count > 0)
        {
            Count += postTimeStamps.Count - commonTimestamps.Count;
            Debug.Log("共通のタイムスタンプ:");
            foreach (var timestamp in commonTimestamps)
            {
                Debug.Log(timestamp.ToString("yyyy-MM-dd HH:mm:ss.fff"));
            }
        }
        else
        {
            Count += preTimeStamps.Count;
            Debug.Log("共通するタイムスタンプはありません。");
        }
    }

    void Update()
    {
        if (shouldUpdateCount)
        {
            shouldUpdateCount = false;  // フラグをリセット

            if (counterController1 != null)
            {
                counterController1.SetCount(Count);  // メインスレッド上で処理
            }
            else
            {
                Debug.LogError("counterControllerがnullです。");
            }
        }
    }
}

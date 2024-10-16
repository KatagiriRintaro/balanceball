using System;
using UnityEngine;
using WebSocketSharp;  // WebSocketSharpライブラリを使用
using System.Collections.Generic;
using System.Linq;
using System.Globalization;
using Newtonsoft.Json.Linq;

public class MainController : MonoBehaviour
{
    private List<DateTime> preTimeStamps1;
    private List<DateTime> preTimeStamps2;
    private List<DateTime> postTimeStamps1;
    public List<DateTime> postTimeStamps2;
    private List<Dictionary<int, string>> playerList = new List<Dictionary<int, string>>();

    private int sendCount1 = 0;
    private int sendCount2 = 0;
    private int Count1 = 0;
    private int Count2 = 0;
    private bool shouldUpdateCount1 = false;
    private bool shouldUpdateCount2 = false;
    private WebSocket wsRegister;
    private WebSocket wsForDataSend;
    public CounterController counterController1;
    public CounterController counterController2;

    private DataProcessor dataProcessor = new DataProcessor();
    private DataProcessor.ProcessedData processedData1;
    private DataProcessor.ProcessedData processedData2;


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

                if (e.Data.Contains("SettingOK"))
                {
                    modifiedData = e.Data.Replace("SettingOK", "");
                }

                else if (e.Data.Contains("SettingNotYet"))
                {
                    modifiedData = e.Data.Replace("SettingNotYet", "");
                }

                Debug.Log(modifiedData);

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
            // Debug.Log("サーバーからのメッセージ: " + e.Data);

            var parsedData = dataProcessor.ParseStringToDynamicList(e.Data);

            int target = dataProcessor.CheckID(playerList, parsedData.Udid.ToString());
            Debug.Log($"Target: {target}");

            try
            {
                if (target == 1)
                {
                    Debug.Log($"CountT1 {Count1}");
                    processedData1 = dataProcessor.Count(parsedData, postTimeStamps1, sendCount1, Count1);
                    preTimeStamps1 = processedData1.preTimeStamps;
                    postTimeStamps1 = processedData1.postTimeStamps;
                    Count1 = processedData1.count;
                    Debug.Log($"CountT1 {Count1}");
                    sendCount1 = processedData1.sendCount;

                    shouldUpdateCount1 = true;
                }

                else if (target == 2)
                {
                    processedData2 = dataProcessor.Count(parsedData, postTimeStamps2, sendCount2, Count2);
                    preTimeStamps2 = processedData2.preTimeStamps;
                    postTimeStamps2 = processedData2.postTimeStamps;
                    Count2 = processedData2.count;
                    sendCount2 = processedData2.sendCount;

                    shouldUpdateCount2 = true;
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
            Debug.Log("WebSocket1接続が閉じられました。");
        };

        // 接続クローズ時のイベント
        wsForDataSend.OnClose += (sender, e) =>
        {
            Debug.Log("WebSocket2接続が閉じられました。");
        };

        // WebSocketに接続
        wsRegister.Connect();
        wsForDataSend.Connect();
    }
    void Update()
    {
        if (shouldUpdateCount1)
        {
            shouldUpdateCount1 = false;  // フラグをリセット

            if (counterController1 != null)
            {
                Debug.Log($"AAA {Count1}");
                counterController1.SetCount(Count1);  // メインスレッド上で処理
            }
            else
            {
                Debug.LogError("counterControllerがnullです。");
            }
        }

        if (shouldUpdateCount2)
        {
            shouldUpdateCount2 = false;  // フラグをリセット

            if (counterController2 != null)
            {
                Debug.Log($"CCC {Count2}");
                counterController2.SetCount(Count2);  // メインスレッド上で処理
            }
            else
            {
                Debug.LogError("counterControllerがnullです。");
            }
        }
    }
}

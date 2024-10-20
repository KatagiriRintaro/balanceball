using System;
using UnityEngine;
using WebSocketSharp;  // WebSocketSharpライブラリを使用
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using System.Text;
using System.Globalization;
using Newtonsoft.Json.Linq;

public class MainController : MonoBehaviour
{
    private List<DateTime> preTimeStamps1;
    private List<DateTime> preTimeStamps2;
    private List<DateTime> postTimeStamps1;
    public List<DateTime> postTimeStamps2;
    private List<Dictionary<int, string>> playerList = new List<Dictionary<int, string>>();

    private List<Dictionary<string, string>> judgeList = new List<Dictionary<string, string>>();

    private int sendCount1 = 0;
    private int sendCount2 = 0;
    private int Count1 = 0;
    private int Count2 = 0;
    private bool shouldUpdateCount1 = false;
    private bool shouldUpdateCount2 = false;

    private bool resetCount = false;
    private bool isReseting = false;
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

                if (string.IsNullOrEmpty(e.Data))
                {
                    return; // 何もしないでリターン
                }

                if (e.Data.Contains("Finish"))
                {
                    Debug.Log($"CC {string.Join(", ", playerList.Select(d => string.Join(", ", d.Select(kvp => $"[{kvp.Key}: {kvp.Value}]"))))}");
                    Debug.Log($"DD {string.Join(", ", judgeList.Select(d => string.Join(", ", d.Select(kvp => $"[{kvp.Key}: {kvp.Value}]"))))}");
                    Dictionary<int, string> firstPlayerData = playerList[0];
                    string value1 = firstPlayerData.Values.First();
                    Dictionary<string, string> firstJudgeData = judgeList[0];
                    Dictionary<int, string> secondPlayerData = playerList[1];
                    string value2 = secondPlayerData.Values.First();
                    Dictionary<string, string> secondJudgeData = judgeList[1];
                    Debug.Log($"1 {Count1} 2 {Count2}");

                    if (Count1 > Count2)
                    {
                        firstJudgeData[value1] = "WIN";
                        secondJudgeData[value2] = "LOSE";
                    }

                    else if (Count2 > Count1)
                    {
                        firstJudgeData[value1] = "LOSE";
                        secondJudgeData[value2] = "WIN";
                    }

                    else
                    {
                        firstJudgeData[value1] = "DRAW";
                        secondJudgeData[value2] = "DRAW";
                    }

                    string jsonString = JsonConvert.SerializeObject(judgeList);
                    wsRegister.Send(jsonString);

                    isReseting = true;

                }

                else if (e.Data.Contains("SettingOK"))
                {
                    modifiedData = e.Data.Replace("SettingOK", "");
                }

                else if (e.Data.Contains("SettingNotYet"))
                {
                    modifiedData = e.Data.Replace("SettingNotYet", "");
                }

                Debug.Log(modifiedData);

                Dictionary<int, string> playerData = new Dictionary<int, string>();  // 辞書を作成
                Dictionary<string, string> judge = new Dictionary<string, string>();


                if (playerList.Count == 0 && modifiedData != "")
                {
                    playerData.Add(1, modifiedData);
                    playerList.Add(playerData);
                    judge.Add(modifiedData, "None");
                    judgeList.Add(judge);
                    Debug.Log($"AA {string.Join(", ", playerList.Select(d => string.Join(", ", d.Select(kvp => $"[{kvp.Key}: {kvp.Value}]"))))}");


                }
                else if (playerList.Count == 1 && modifiedData != "")
                {
                    playerData.Add(2, modifiedData);
                    playerList.Add(playerData);
                    judge.Add(modifiedData, "None");
                    judgeList.Add(judge);
                    Debug.Log($"BB {string.Join(", ", playerList.Select(d => string.Join(", ", d.Select(kvp => $"[{kvp.Key}: {kvp.Value}]"))))}");

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

            var parsedData = dataProcessor.ParseStringToDynamicList(e.Data);

            int target = dataProcessor.CheckID(playerList, parsedData.Udid.ToString());

            try
            {
                if (target == 1)
                {
                    processedData1 = dataProcessor.Count(parsedData, postTimeStamps1, sendCount1, Count1);
                    preTimeStamps1 = processedData1.preTimeStamps;
                    postTimeStamps1 = processedData1.postTimeStamps;
                    Count1 = processedData1.count;
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

        if (resetCount)
        {
            resetCount = false;

            if (counterController1 != null && counterController2 != null)
            {
                counterController1.SetCount(0);
                counterController2.SetCount(0);

            }
            else
            {
                Debug.LogError("counterControllerがnullです。");
            }
        }

        if (isReseting)
        {
            ResetAll();
        }
    }

    void ResetAll()
    {
        isReseting = false;
        resetCount = true;
        Count1 = 0;
        Count2 = 0;
        preTimeStamps1.Clear();
        preTimeStamps2.Clear();
        postTimeStamps1.Clear();
        postTimeStamps2.Clear();
        playerList.Clear();
        judgeList.Clear();
    }
}

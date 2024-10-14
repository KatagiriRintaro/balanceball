using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using Newtonsoft.Json.Linq;
using UnityEngine;

public class DataProcessor
{
    public class ParsedData
    {
        public List<DateTime> TimeStamps { get; set; }
        public string Udid { get; set; }

        public ParsedData()
        {
            TimeStamps = new List<DateTime>();
        }
    }

    public class ProcessedData
    {
        public List<DateTime> preTimeStamps { get; set; }

        public List<DateTime> postTimeStamps { get; set; }
        public int count { get; set; }
        public int sendCount { get; set; }

        public ProcessedData()
        {
            preTimeStamps = new List<DateTime>();
            postTimeStamps = new List<DateTime>();
        }
    }

    public int CheckID(List<Dictionary<int, string>> playerList, string targetValue)
    {
        int targetKey = -1;

        foreach (var dictionary in playerList)
        {
            foreach (var kvp in dictionary)
            {
                string stringValue = kvp.Value.Replace("\"", "");
                if (stringValue == targetValue)
                {
                    targetKey = kvp.Key;
                    break;
                }
            }
            if (targetKey != -1)
            {
                break;
            }
        }
        return targetKey;
    }

    public ParsedData ParseStringToDynamicList(string data)
    {
        ParsedData parsedData = new ParsedData();

        try
        {
            // JSONを解析してTimeStampsを取得
            JObject jsonData = JObject.Parse(data);
            parsedData.Udid = jsonData["udid"]?.ToString();
            // Debug.Log("Udid: " + parsedData.Udid);
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
                    parsedData.TimeStamps.Add(parsedDate);
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

        return parsedData;
    }

    public ProcessedData Count(ParsedData parsedData, List<DateTime> postTimeStamps, int sendCount, int count)
    {
        ProcessedData processedData = new ProcessedData();

        if (sendCount == 0)
        {
            processedData.postTimeStamps = parsedData.TimeStamps;  // TimeStamps プロパティを取得して代入
            string postTimeStampsString = string.Join(", ", processedData.postTimeStamps.Select(ts => ts.ToString("yyyy-MM-dd HH:mm:ss.fff")));
            Debug.Log("postTimeStamps: " + postTimeStampsString);
            processedData.sendCount = 1;
            count += processedData.postTimeStamps.Count;
            processedData.count = count;
        }
        else
        {
            processedData.preTimeStamps = DeepCopyDynamicList(postTimeStamps);
            processedData.postTimeStamps = parsedData.TimeStamps;  // TimeStamps プロパティを取得して代入

            processedData.count = CompareTimestamps(processedData.preTimeStamps, processedData.postTimeStamps, count);
            processedData.sendCount = 1;
        }

        return processedData;
    }

    public List<DateTime> DeepCopyDynamicList(List<DateTime> source)
    {
        return new List<DateTime>(source);
    }

    public int CompareTimestamps(List<DateTime> preTimeStamps, List<DateTime> postTimeStamps, int Count)
    {
        // string preTimeStampsString = string.Join(", ", preTimeStamps.Select(ts => ts.ToString("yyyy-MM-dd HH:mm:ss.fff")));
        // Debug.Log("preTimeStamps: " + preTimeStampsString);
        // string postTimeStampsString = string.Join(", ", postTimeStamps.Select(ts => ts.ToString("yyyy-MM-dd HH:mm:ss.fff")));
        // Debug.Log("postTimeStamps: " + postTimeStampsString);
        // postTimeStamps と preTimeStamps の共通要素を取得
        var commonTimestamps = preTimeStamps.Intersect(postTimeStamps).ToList();

        // 共通部分のログ出力
        if (commonTimestamps.Count > 0)
        {
            Debug.Log($"PreCount {Count}");
            Count += postTimeStamps.Count - commonTimestamps.Count;
            Debug.Log($"PostCount {Count}");
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

        return Count;
    }
}

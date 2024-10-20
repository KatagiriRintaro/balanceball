using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class CounterController : MonoBehaviour
{
    public Color LightColor;
    public Color Black = Color.black;

    // private int Count = 0;
    private int onesPlace = 0;
    private int tensPlace = 0;
    private int hundredsPlace = 0;

    void Start()
    {
        GameObject[] blackObjects = gameObject.GetComponentsInChildren<Transform>()
        .Where(t => t != gameObject.transform && t.gameObject.name != "device")  // 自分自身を除外
        .Select(t => t.gameObject)              // Transform を GameObject に変換
        .ToArray();                             // 配列に変換

        foreach (GameObject obj in blackObjects)
        {
            // オブジェクト内の全てのRendererコンポーネントを取得
            Renderer[] renderers = obj.GetComponentsInChildren<Renderer>();

            foreach (Renderer renderer in renderers)
            {
                if (renderer.gameObject == obj)
                {
                    continue;
                }

                if (renderer != null)
                {
                    renderer.material.color = Black;
                }
                else
                {
                    Debug.Log("Renderer was null");
                }
            }
        }

        SetCount(0);
    }

    public void SetCount(int count)
    {
        Debug.Log("Count is set to: " + count);

        // Countが更新されたら表示をアップデート
        onesPlace = count % 10;
        tensPlace = count / 10 % 10;
        hundredsPlace = count / 100 % 10;
        Debug.Log($"1 {onesPlace} 10 {tensPlace} 100 {hundredsPlace}");

        UpdateNumberDisplay("OnesPlace", onesPlace);

        if (count >= 10)
        {
            UpdateNumberDisplay("TensPlace", tensPlace);
        }
        if (count >= 100)
        {
            UpdateNumberDisplay("HundredsPlace", hundredsPlace);
        }

        // Debug.Log("ASA");
    }

    void UpdateNumberDisplay(string placeTag, int number)
    {
        // GameObject[] placeObjects = GameObject.FindGameObjectsWithTag(placeTag);
        Transform[] placeObjects = GetComponentsInChildren<Transform>()
        .Where(t => t.gameObject.CompareTag(placeTag))  // タグでフィルタリング
        .ToArray();

        if (placeObjects != null && placeObjects.Length > 0)
        {
            // foreach (GameObject placeObject in placeObjects)
            foreach (Transform placeObject in placeObjects)
            {

                // placeObject 内の NumberTextController を取得
                // NumberTextController numberTextController = placeObject.GetComponent<NumberTextController>();
                NumberTextController numberTextController = placeObject.GetComponent<NumberTextController>();

                // if (numberTextController != null)
                if (numberTextController != null)
                {
                    // 任意のフィールドやプロパティを出力する例
                    // numberTextController.ChangeNumber(number);
                    numberTextController.ChangeNumber(number);
                }
                else
                {
                    Debug.LogWarning($"'{placeTag}' の子オブジェクトに 'NumberTextController' が見つかりませんでした。");
                }
            }
        }
        else
        {
            Debug.LogWarning($"'{placeTag}' タグが付いたオブジェクトが見つかりませんでした。");
        }
    }
}

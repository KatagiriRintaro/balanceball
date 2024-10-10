using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class NumberTextController : MonoBehaviour
{
    GameObject[] RightTop;
    GameObject[] RightBottom;
    GameObject[] CenterTop;
    GameObject[] CenterMiddle;
    GameObject[] CenterBottom;
    GameObject[] LeftTop;
    GameObject[] LeftBottom;

    void Start()
    {
        // このスクリプトが BlackNumberText にアタッチされていると仮定し、その子オブジェクトのみを探索
        GameObject blackNumberText = GameObject.FindGameObjectWithTag("BlackNumberText"); // BlackNumberText オブジェクトを取得

        if (blackNumberText != null)
        {
            RightTop = GetChildrenWithTag(blackNumberText.transform, "RightTop");
            RightBottom = GetChildrenWithTag(blackNumberText.transform, "RightBottom");
            CenterTop = GetChildrenWithTag(blackNumberText.transform, "CenterTop");
            CenterMiddle = GetChildrenWithTag(blackNumberText.transform, "CenterMiddle");
            CenterBottom = GetChildrenWithTag(blackNumberText.transform, "CenterBottom");
            LeftTop = GetChildrenWithTag(blackNumberText.transform, "LeftTop");
            LeftBottom = GetChildrenWithTag(blackNumberText.transform, "LeftBottom");
        }
        else
        {
            Debug.LogError("BlackNumberText オブジェクトが見つかりませんでした。");
        }
    }

    public void ChangeNumber(int number)
    {

        SetObjectsActive(RightTop, true); SetObjectsActive(RightBottom, true); SetObjectsActive(CenterTop, true); SetObjectsActive(CenterMiddle, true);
        SetObjectsActive(CenterBottom, true); SetObjectsActive(LeftTop, true); SetObjectsActive(LeftBottom, true);

        switch (number)
        {
            case 0:
                SetObjectsActive(RightTop, false); SetObjectsActive(RightBottom, false); SetObjectsActive(CenterTop, false); SetObjectsActive(CenterBottom, false);
                SetObjectsActive(LeftTop, false); SetObjectsActive(LeftBottom, false);
                break;

            case 1:
                SetObjectsActive(RightTop, false); SetObjectsActive(RightBottom, false);
                break;

            case 2:
                SetObjectsActive(RightTop, false); SetObjectsActive(CenterTop, false); SetObjectsActive(CenterMiddle, false); SetObjectsActive(CenterBottom, false);
                SetObjectsActive(LeftBottom, false);
                break;

            case 3:
                SetObjectsActive(RightTop, false); SetObjectsActive(RightBottom, false); SetObjectsActive(CenterTop, false); SetObjectsActive(CenterMiddle, false);
                SetObjectsActive(CenterBottom, false);
                break;

            case 4:
                SetObjectsActive(RightTop, false); SetObjectsActive(RightBottom, false); SetObjectsActive(CenterMiddle, false); SetObjectsActive(LeftTop, false);
                break;

            case 5:
                SetObjectsActive(RightBottom, false); SetObjectsActive(CenterTop, false); SetObjectsActive(CenterMiddle, false); SetObjectsActive(CenterBottom, false);
                SetObjectsActive(LeftTop, false);
                break;

            case 6:
                SetObjectsActive(RightBottom, false); SetObjectsActive(CenterTop, false); SetObjectsActive(CenterMiddle, false); SetObjectsActive(CenterBottom, false);
                SetObjectsActive(LeftTop, false); SetObjectsActive(LeftBottom, false);
                break;

            case 7:
                SetObjectsActive(RightTop, false); SetObjectsActive(RightBottom, false); SetObjectsActive(CenterTop, false); SetObjectsActive(LeftTop, false);
                break;

            case 8:
                SetObjectsActive(RightTop, false); SetObjectsActive(RightBottom, false); SetObjectsActive(CenterTop, false); SetObjectsActive(CenterMiddle, false);
                SetObjectsActive(CenterBottom, false); SetObjectsActive(LeftTop, false); SetObjectsActive(LeftBottom, false);
                break;

            case 9:
                SetObjectsActive(RightTop, false); SetObjectsActive(RightBottom, false); SetObjectsActive(CenterTop, false); SetObjectsActive(CenterMiddle, false);
                SetObjectsActive(CenterBottom, false); SetObjectsActive(LeftBottom, false);
                break;
                ;
            default:
                break;
        }
    }

    void SetObjectsActive(GameObject[] objects, bool active)
    {
        if (objects == null || objects.Length == 0) return;

        foreach (GameObject obj in objects)
        {
            obj.SetActive(active);
        }
    }

    GameObject[] GetChildrenWithTag(Transform parent, string tag)
    {
        // 親オブジェクトの子オブジェクトすべてを取得し、タグでフィルタリング
        GameObject[] childrenWithTag = parent.GetComponentsInChildren<Transform>()
            .Where(t => t.gameObject.CompareTag(tag))  // タグが一致するものだけを選択
            .Select(t => t.gameObject)                 // Transform を GameObject に変換
            .ToArray();                                // 配列として取得

        // 子オブジェクトの個数を表示
        Debug.Log($"'{tag}' タグの子オブジェクトの個数: {childrenWithTag.Length}");

        return childrenWithTag;  // 配列を返す
    }

}

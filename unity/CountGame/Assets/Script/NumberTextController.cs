using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class ChangeNumberTextController : MonoBehaviour
{
    // Start is called before the first frame update

    public Color LightColor;
    public GameObject[] RightTop;
    public GameObject[] RightBottom;
    public GameObject[] CenterTop;
    public GameObject[] CenterMiddle;
    public GameObject[] CenterBottom;
    public GameObject[] LeftTop;
    public GameObject[] LeftBottom;
    void Start()
    {
        Transform parentTransform = gameObject.transform;

        // Check for children with specific tags
        RightTop = GetChildrenWithTag(parentTransform, "RightTop");
        RightBottom = GetChildrenWithTag(parentTransform, "RightBottom");
        CenterTop = GetChildrenWithTag(parentTransform, "CenterTop");
        CenterMiddle = GetChildrenWithTag(parentTransform, "CenterMiddle");
        CenterBottom = GetChildrenWithTag(parentTransform, "CenterBottom");
        LeftTop = GetChildrenWithTag(parentTransform, "LeftTop");
        LeftBottom = GetChildrenWithTag(parentTransform, "LeftBottom");
    }


    public void ChangeNumber(int number)
    {
        SetObjectsColor(RightTop, Color.black); SetObjectsColor(RightBottom, Color.black); SetObjectsColor(CenterTop, Color.black); SetObjectsColor(CenterMiddle, Color.black);
        SetObjectsColor(CenterBottom, Color.black); SetObjectsColor(LeftTop, Color.black); SetObjectsColor(LeftBottom, Color.black);

        switch (number)
        {
            case 0:
                SetObjectsColor(RightTop, LightColor); SetObjectsColor(RightBottom, LightColor); SetObjectsColor(CenterTop, LightColor); SetObjectsColor(CenterBottom, LightColor);
                SetObjectsColor(LeftTop, LightColor); SetObjectsColor(LeftBottom, LightColor);
                break;

            case 1:
                SetObjectsColor(RightTop, LightColor); SetObjectsColor(RightBottom, LightColor);
                break;

            case 2:
                SetObjectsColor(RightTop, LightColor); SetObjectsColor(CenterTop, LightColor); SetObjectsColor(CenterMiddle, LightColor); SetObjectsColor(CenterBottom, LightColor);
                SetObjectsColor(LeftBottom, LightColor);
                break;

            case 3:
                SetObjectsColor(RightTop, LightColor); SetObjectsColor(RightBottom, LightColor); SetObjectsColor(CenterTop, LightColor); SetObjectsColor(CenterMiddle, LightColor);
                SetObjectsColor(CenterBottom, LightColor);
                break;

            case 4:
                SetObjectsColor(RightTop, LightColor); SetObjectsColor(RightBottom, LightColor); SetObjectsColor(CenterMiddle, LightColor); SetObjectsColor(LeftTop, LightColor);
                break;

            case 5:
                SetObjectsColor(RightBottom, LightColor); SetObjectsColor(CenterTop, LightColor); SetObjectsColor(CenterMiddle, LightColor); SetObjectsColor(CenterBottom, LightColor);
                SetObjectsColor(LeftTop, LightColor);
                break;

            case 6:
                SetObjectsColor(RightBottom, LightColor); SetObjectsColor(CenterTop, LightColor); SetObjectsColor(CenterMiddle, LightColor); SetObjectsColor(CenterBottom, LightColor);
                SetObjectsColor(LeftTop, LightColor); SetObjectsColor(LeftBottom, LightColor);
                break;

            case 7:
                SetObjectsColor(RightTop, LightColor); SetObjectsColor(RightBottom, LightColor); SetObjectsColor(CenterTop, LightColor); SetObjectsColor(LeftTop, LightColor);
                break;

            case 8:
                SetObjectsColor(RightTop, LightColor); SetObjectsColor(RightBottom, LightColor); SetObjectsColor(CenterTop, LightColor); SetObjectsColor(CenterMiddle, LightColor);
                SetObjectsColor(CenterBottom, LightColor); SetObjectsColor(LeftTop, LightColor); SetObjectsColor(LeftBottom, LightColor);
                break;

            case 9:
                SetObjectsColor(RightTop, LightColor); SetObjectsColor(RightBottom, LightColor); SetObjectsColor(CenterTop, LightColor); SetObjectsColor(CenterMiddle, LightColor);
                SetObjectsColor(CenterBottom, LightColor); SetObjectsColor(LeftTop, LightColor);
                break;

            default:
                break;
        }
    }
    void SetObjectsColor(GameObject[] objects, Color color)
    {
        if (objects == null || objects.Length == 0) return;

        foreach (GameObject obj in objects)
        {
            // オブジェクトとその子オブジェクトすべてのRendererを取得して色を変更
            Renderer[] renderers = obj.GetComponentsInChildren<Renderer>();  // 親とすべての子のRendererを取得
            foreach (Renderer renderer in renderers)
            {
                if (renderer != null)
                {
                    // マテリアルの新しいインスタンスを作成して色を変更
                    renderer.material = new Material(renderer.material);
                    renderer.material.color = color;
                }
            }
        }
    }


    GameObject[] GetChildrenWithTag(Transform parent, string tag)
    {
        // 親オブジェクトの子オブジェクトすべてを取得し、タグでフィルタリング
        GameObject[] childrenWithTag = parent.GetComponentsInChildren<Transform>()
            .Where(t => t.gameObject.CompareTag(tag))  // タグが一致するものだけを選択
            .Select(t => t.gameObject)                 // Transform を GameObject に変換
            .ToArray();                                // 配列として取得

        return childrenWithTag;  // 配列を返す
    }


}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CounterController : MonoBehaviour
{
    public Color LightColor;
    public Color Black = Color.black;

    void Start()
    {
        // "LightNumberText" タグを持つオブジェクトを探し、色を変更
        GameObject[] lightObjects = GameObject.FindGameObjectsWithTag("LightNumberText");
        foreach (GameObject obj in lightObjects)
        {
            // オブジェクト内の全てのRendererコンポーネントを取得
            Renderer[] renderers = obj.GetComponentsInChildren<Renderer>();
            foreach (Renderer renderer in renderers)
            {
                if (renderer != null)
                {
                    // Rendererが見つかったら色を変更
                    renderer.material.color = LightColor;
                }
            }
        }

        // "BlackNumberText" タグを持つオブジェクトを探し、色を変更
        GameObject[] blackObjects = GameObject.FindGameObjectsWithTag("BlackNumberText");
        foreach (GameObject obj in blackObjects)
        {
            // オブジェクト内の全てのRendererコンポーネントを取得
            Renderer[] renderers = obj.GetComponentsInChildren<Renderer>();
            foreach (Renderer renderer in renderers)
            {
                if (renderer != null)
                {
                    // Rendererが見つかったら色を変更
                    renderer.material.color = Black;
                }
            }
        }
    }
}

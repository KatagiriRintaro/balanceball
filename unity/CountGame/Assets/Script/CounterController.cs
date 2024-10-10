using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CounterController : MonoBehaviour
{
    public Color LightColor;
    public Color Black = Color.black;

    private int count = 0;
    private int onesPlace = 0;
    private int tensPlace = 0;
    private int hundredsPlace = 0;

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
        Debug.Log("" + blackObjects.Length);
        foreach (GameObject obj in blackObjects)
        {
            // オブジェクト内の全てのRendererコンポーネントを取得
            Renderer[] renderers = obj.GetComponentsInChildren<Renderer>();
            Debug.Log($"{obj.name} has {renderers.Length} renderers.");

            foreach (Renderer renderer in renderers)
            {
                if (renderer != null)
                {
                    // Rendererが見つかったら色を変更
                    renderer.material.color = Black;
                }
                else
                {
                    Debug.Log("Renderer was null");
                }
            }
        }
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            count++;
            onesPlace = count % 10;
            tensPlace = (count / 10) % 10;
            hundredsPlace = (count / 100) % 10;

            UpdateNumberDisplay("OnesPlace", onesPlace);

            if (count >= 10)
            {
                UpdateNumberDisplay("TensPlace", tensPlace);

            }
            if (count >= 100)
            {
                UpdateNumberDisplay("HundredsPlace", hundredsPlace);

            }
        }
    }

    void UpdateNumberDisplay(string placeTag, int number)
    {
        GameObject[] placeObjects = GameObject.FindGameObjectsWithTag(placeTag);

        if (placeObjects != null && placeObjects.Length > 0)
        {
            foreach (GameObject placeObject in placeObjects)
            {
                // placeObject 内の NumberTextController を取得
                NumberTextController numberTextController = placeObject.GetComponent<NumberTextController>();

                if (numberTextController != null)
                {
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

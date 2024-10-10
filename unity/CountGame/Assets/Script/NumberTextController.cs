using System.Collections;
using System.Collections.Generic;
using UnityEngine;

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
        RightTop = GameObject.FindGameObjectsWithTag("RightTop");
        RightBottom = GameObject.FindGameObjectsWithTag("RightBottom");
        CenterTop = GameObject.FindGameObjectsWithTag("CenterTop");
        CenterMiddle = GameObject.FindGameObjectsWithTag("CenterMiddle");
        CenterBottom = GameObject.FindGameObjectsWithTag("CenterBottom");
        LeftTop = GameObject.FindGameObjectsWithTag("LeftTop");
        LeftBottom = GameObject.FindGameObjectsWithTag("LeftBottom");
    }

    public void ChangeNumber(int number)
    {
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
                SetObjectsActive(LeftBottom, false);
                break;

            case 4:
                SetObjectsActive(RightTop, false); SetObjectsActive(RightBottom, false); SetObjectsActive(CenterMiddle, false); SetObjectsActive(LeftTop, false);
                SetObjectsActive(LeftBottom, false);
                break;

            case 5:
                SetObjectsActive(RightBottom, false); SetObjectsActive(CenterTop, false); SetObjectsActive(CenterMiddle, false); SetObjectsActive(CenterBottom, false);
                SetObjectsActive(LeftBottom, false);
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
                SetObjectsActive(CenterMiddle, false); SetObjectsActive(LeftTop, false); SetObjectsActive(LeftBottom, false);
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
        foreach (GameObject obj in objects)
        {
            obj.SetActive(active);
        }
    }
}

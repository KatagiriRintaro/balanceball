import numpy as np

train_name = ['hamstring_curl', 'press_up', "knee_extension", "pike", "skier", "abdominal_crunch"]
weight_class = [5,6,7]
balance_feature_class = ['左右差なし', '右', '左']
balance_class = [1,2,3,4]


def Make_Class(all_training_feature_df ,class_name):

    if class_name == 'subject_weight':
        Classlabel = np.zeros([len(all_training_feature_df), 3])
    elif class_name == 'balance':
        Classlabel = np.zeros([len(all_training_feature_df), 4])
    else:
        Classlabel = np.zeros([len(all_training_feature_df), all_training_feature_df[class_name].nunique()])

    for i in range(len(all_training_feature_df[class_name])):
        if class_name == 'class':
            Classlabel[i, :] = np.zeros([1, 6])
            Classlabel[i, train_name.index(all_training_feature_df["class"][i])] = 1
        elif class_name == 'subject_weight':
            Classlabel[i, :] = np.zeros([1, 3])
            tens_digit = float(all_training_feature_df['subject_weight'][i]//10)
            Classlabel[i, weight_class.index(tens_digit)] = 1
        elif class_name == 'balance_feature':
            Classlabel[i, :] = np.zeros([1, 3])
            Classlabel[i, train_name.index(all_training_feature_df['balance_feature'][i])] = 1
        elif class_name == 'balance':
            Classlabel[i, :] = np.zeros([1, 4])
            digit = int(float(all_training_feature_df['subject_weight'][i]))
            Classlabel[i, weight_class.index(digit)] = 1
        else:
            print("Error")
    
    return Classlabel
        
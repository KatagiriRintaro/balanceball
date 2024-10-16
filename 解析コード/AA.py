def LOGO(X,Y, groups, number):
  labels = np.unique(Y)
  classifiers = [
                ("RF", RandomForestClassifier(random_state=0)),
               ("ANN", MLPClassifier()),
               ("LR", LogisticRegression()),
               ("DT", DecisionTreeClassifier()),
               ("NB", GaussianNB()),
               ("SVM", SVC()),
               ("KNN", KNeighborsClassifier())
               ]

  name, clf = classifiers[number]
  scaler = StandardScaler()
  #pca = PCA(n_components=0.95)
  pipeline = make_pipeline(scaler, clf)

  cv = LeaveOneGroupOut()
  # cv = StratifiedKFold(10, shuffle=True)
  y_pred = cross_val_predict(pipeline, X, Y,
                            groups= groups,
                            cv=cv,
                            n_jobs=1, verbose=1)
  cr_dict = classification_report(Y, y_pred, output_dict=True)
  accuracy = cr_dict['accuracy']
  # print(classification_report(Y, y_pred))
  # cm = confusion_matrix(Y, y_pred, labels=labels)
  # cm_df = pd.DataFrame(cm, index=labels, columns=labels)
  # generate_cm(cm_df, index=labels, columns=labels)
  return accuracy

def KFold(X, Y, number):
    labels = np.unique(Y)
    classifiers = [
        ("RF", RandomForestClassifier(random_state=0)),
        ("ANN", MLPClassifier()),
        ("LR", LogisticRegression()),
        ("DT", DecisionTreeClassifier()),
        ("NB", GaussianNB()),
        ("SVM", SVC()),
        ("KNN", KNeighborsClassifier())
    ]

    name, clf = classifiers[number]
    scaler = StandardScaler()
    pipeline = make_pipeline(scaler, clf)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

    accuracies = []
    all_y_true = []
    all_y_pred = []

    for train_index, test_index in cv.split(X, Y):
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]

        pipeline.fit(X_train, Y_train)
        y_pred = pipeline.predict(X_test)

        accuracies.append(np.mean(y_pred == Y_test))
        all_y_true.extend(Y_test)
        all_y_pred.extend(y_pred)

    cr_dict = classification_report(all_y_true, all_y_pred, output_dict=True)
    accuracy = np.mean(accuracies)
    # print(classification_report(all_y_true, all_y_pred))

    # cm = confusion_matrix(all_y_true, all_y_pred, labels=labels)
    # cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    # generate_cm(cm_df, index=labels, columns=labels)

    return accuracy



def LOGO_LightGBM(X, Y, groups):
  logo = LeaveOneGroupOut()

  accuracies = []
  for train_index, test_index in logo.split(X, Y, groups):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = Y[train_index], Y[test_index]

    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    params = {
        'objective': 'multiclass',
        'num_class':  len(np.unique(Y)),
        'metric': 'multi_logloss',
        'num_leaves': 20,
        'learning_rate': 0.05,
        'feature_fraction': 0.9
    }

    num_round = 100
    bst = lgb.train(params, train_data, num_round, valid_sets=[test_data])

    y_pred = bst.predict(X_test)
    y_pred_labels = np.argmax(y_pred, axis=1)

    accuracy = accuracy_score(y_test, y_pred_labels)
    accuracies.append(accuracy)
  return np.mean(accuracies)

def KFold_LightGBM(X, Y):
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    print("AA",len(np.unique(Y)))

    accuracies = []
    for train_index, test_index in skf.split(X, Y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = Y[train_index], Y[test_index]

        train_data = lgb.Dataset(X_train, label=y_train)
        test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

        params = {
            'objective': 'multiclass',
            'num_class': len(np.unique(Y)),
            'metric': 'multi_logloss',
            'num_leaves': 20,
            'learning_rate': 0.05,
            'feature_fraction': 0.9
        }

        num_round = 100
        bst = lgb.train(params, train_data, num_round, valid_sets=[test_data])

        y_pred = bst.predict(X_test)
        y_pred_labels = np.argmax(y_pred, axis=1)

        accuracy = accuracy_score(y_test, y_pred_labels)
        accuracies.append(accuracy)

    return np.mean(accuracies)

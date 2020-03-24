# the actual label file path
f_actual_label = open("data/l3.txt", "r")
# the predicted label file path
f_predicted_label = open("data/power_vad_result.txt")

# frame size in ms
frame_size_ml = 50
# length of the audio file in sec
file_len_sec = 90

TP = 0
FP = 0
FN = 0
TN = 0

actual_label = []
predicted_label = []
actual_data = []
prediction_data = []


def create_data():
    global actual_data
    global prediction_data

    for i in f_actual_label:
        temp = i.split('\t')
        line = [int(float(temp[0]) * 1000), int(float(temp[1]) * 1000)]
        actual_label.append(line)

    for i in f_predicted_label:
        temp = i.split('\t')
        line = [int(float(temp[0]) * 1000), int(float(temp[1]) * 1000)]
        predicted_label.append(line)

    for i in range(0, file_len_sec * 1000 + frame_size_ml, frame_size_ml):
        fl = 0
        for j in range(0, len(actual_label)):
            if actual_label[j][0] <= i <= actual_label[j][1]:
                actual_data.append('1')
                fl = 1
                break
        if fl == 0:
            actual_data.append('0')

        fl1 = 0
        for j in range(0, len(predicted_label)):
            if predicted_label[j][0] <= i <= predicted_label[j][1]:
                prediction_data.append('1')
                fl1 = 1
                break
        if fl1 == 0:
            prediction_data.append('0')


# f_actual = open("data/actual.txt", "r")
# f_prediction = open("data/prediction.txt", "r")

# actual_data = f_actual.read().split(' ')
# prediction_data = f_prediction.read().split(' ')


def is_TP(actual, prediction):
    if prediction == '1' and actual == '1':
        return True
    else:
        return False


def is_FP(actual, prediction):
    if prediction == '1' and actual == '0':
        return True
    else:
        return False


def is_FN(actual, prediction):
    if prediction == '0' and actual == '1':
        return True
    else:
        return False


def is_TN(actual, prediction):
    if prediction == '0' and actual == '0':
        return True
    else:
        return False


def print_all():
    print(actual_label)
    print(predicted_label)

    for i in actual_data:
        print(i, end=' ')
    print("")

    for i in prediction_data:
        print(i, end=' ')
    print("\n")


def calculate():
    for i in range(0, len(actual_data)):
        if is_TP(actual_data[i], prediction_data[i]):
            global TP
            TP = TP + 1
            global TN
            global FN

            l_fn = 0
            l_fp = 0
            for j in reversed(range(0, i)):
                if is_FN(actual_data[j], prediction_data[j]):
                    l_fn = l_fn + 1
                else:
                    break

            global FN
            FN = FN - l_fn
            global TN
            TN = TN + l_fn

            for j in reversed(range(0, i)):
                if is_FP(actual_data[j], prediction_data[j]):
                    l_fp += 1
                else:
                    break

            global FP
            FP -= l_fp
            TP += l_fp

        elif is_FN(actual_data[i], prediction_data[i]):
            FN = FN + 1
            if is_TP(actual_data[i - 1], prediction_data[i - 1]) and i > 0:
                prediction_data[i] = '1'
                FN -= 1
                TN += 1

        elif is_FP(actual_data[i], prediction_data[i]):
            FP = FP + 1
            if is_TP(actual_data[i - 1], prediction_data[i - 1]) and i > 0:
                actual_data[i] = '1'
                FP -= 1
                TP += 1

        elif is_TN(actual_data[i], prediction_data[i]):
            TN = TN + 1

    print("TP = " + str(TP))
    print("FN = " + str(FN))
    print("FP = " + str(FP))
    print("TN = " + str(TN))

    if TP + FP > 0:
        print("Precision = " + str(TP / (TP + FP)))
    else:
        print("Precision is extremely low")
    if TP + FN > 0:
        print("Recall = " + str(TP / (TP + FN)))
    else:
        print("Recall is extremely low")


create_data()
print_all()
calculate()

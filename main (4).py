from data_representation import DataTable
from predictors import MajorityClassPredictor, NearestNeighborPredictor
from exceptions import OutOfSampleError


def make_case(row_dict):
    #this function makes sure we return a dict with those features as floats
    case = {}
    for i in range(1, 10):
        feat = "Feature" + str(i)
        case[feat] = float(row_dict[feat])
    return case


def accuracy(preds, labels):
    correct = 0
    for i in range(len(labels)):
        if preds[i] == labels[i]:
            correct += 1
    return correct / len(labels)


def main():

    historical_path = "cancer_historical.csv"
    new_cases_path = "cancer_new_cases.csv"
    labels_path = "cancer_new_cases_labels.csv"

    historical = DataTable(historical_path)
    new_cases = DataTable(new_cases_path)
    labels_table = DataTable(labels_path)

    majority = MajorityClassPredictor(historical)
    nearest = NearestNeighborPredictor(historical)

    majority_preds = []
    nearest_preds = []

    # predict each new case
    for i in range(len(new_cases.data)):
        row = new_cases.get_row(i)
        case = make_case(row)

        # out of sample check 
        try:
            majority.check_ranges(case)
        except OutOfSampleError as e:
            print("OutOfSampleError:", e)
            return

        maj_pred = majority.predict(case)
        nn_pred = nearest.predict(case)

        majority_preds.append(maj_pred)
        nearest_preds.append(nn_pred)

        # Suggested print style (simple)
        print("Case", i + 1, ": Majority =", maj_pred, "NearestNeighbor =", nn_pred)

    # evaluation
    #Having trouble calling 'TumorType'
    label_col = labels_table.get_column_names()[0]   # first column
    true_labels = labels_table.get_column(label_col)

    maj_acc = accuracy(majority_preds, true_labels)
    nn_acc = accuracy(nearest_preds, true_labels)

    print("MajorityClassPredictor:", round(maj_acc, 3))
    print("NearestNeighborPredictor:", round(nn_acc, 3))


if __name__ == "__main__":
    main()
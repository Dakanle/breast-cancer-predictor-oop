import math
from exceptions import OutOfSampleError

class Predictor:
    def __init__(self, reference_data):
        self.reference_data = reference_data
        self.features = []
        for i in range(1, 10):
            self.features.append("Feature" + str(i))

        self.ranges = {}
        for feat in self.features:
            mn = self.reference_data.get_column_min(feat)
            mx = self.reference_data.get_column_max(feat)
            self.ranges[feat] = (mn, mx)

    # range checking function
    def check_ranges(self, new_case):
        for feat in self.features:
            val = new_case[feat]
            mn, mx = self.ranges[feat]
            if val < mn or val > mx:
                raise OutOfSampleError(
                    f"{feat} with value {val} is outside historical range [{mn}, {mx}]"
                )


class MajorityClassPredictor(Predictor):
    def __init__(self, reference_data):
        super().__init__(reference_data)

        labels = self.reference_data.get_column("TumorType")

        count_0 = 0
        count_1 = 0
        for y in labels:
            if y == 0:
                count_0 += 1
            else:
                count_1 += 1

        if count_1 > count_0:
            self.majority = 1
        else:
            self.majority = 0

    def predict(self, new_case):
        return self.majority

class NearestNeighborPredictor(Predictor):
    def __init__(self, reference_data):
        super().__init__(reference_data)

    def predict(self, new_case):
        best_dist = None
        best_label = None

        for row in self.reference_data.data:
            total = 0.0
            for feat in self.features:
                diff = new_case[feat] - row[feat]
                total += diff * diff

            dist = math.sqrt(total)

            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_label = row["TumorType"]

        return best_label
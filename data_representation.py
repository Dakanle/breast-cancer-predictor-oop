class DataTable:
    def __init__(self, csv_path: str):
        self.data = []

        with open(csv_path, "r", encoding="utf-8") as f:
            # list of the headers
            header = f.readline().strip().split(",")
            self.columns = header

            for line in f:
                values = line.strip().split(",")

                row_dict = {}
                for i in range(len(header)):
                    col = header[i]
                    val = values[i]

                    # convert types
                    if col == "TumorType":
                        row_dict[col] = int(val)
                    else:
                        row_dict[col] = float(val)

                self.data.append(row_dict)

    
    def get(self, row_idx, col_name):
        return self.data[row_idx][col_name]

    def get_column(self, col_name):
        column_list = []
        for row in self.data:
            column_list.append(row[col_name])
        return column_list

    def get_row(self, row_idx):
        return self.data[row_idx]

    def get_column_names(self):
        return self.columns

    def get_column_average(self, col_name):
        column = self.get_column(col_name)
        total = 0
        for value in column:
            total += value
        return total / len(column)

    def get_column_min(self, col_name):
        column = self.get_column(col_name)
        smallest = column[0]
        for value in column:
            if value < smallest:
                smallest = value
        return smallest

    def get_column_max(self, col_name):
        column = self.get_column(col_name)
        largest = column[0]
        for value in column:
            if value > largest:
                largest = value
        return largest
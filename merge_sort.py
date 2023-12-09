class MergeSortDict:
    def __init__(self, input_dict):
        self.input_dict = input_dict

    def merge_sort(self, by_key=True, ascending=True, value_index=0):
        items = list(self.input_dict.items())
        sorted_items = self._merge_sort(items, by_key, ascending, value_index)
        sorted_dict = dict(sorted_items)
        return sorted_dict

    def _merge_sort(self, items, by_key, ascending, value_index):
        if len(items) <= 1:
            return items

        mid = len(items) // 2
        left = self._merge_sort(items[:mid], by_key, ascending, value_index)
        right = self._merge_sort(items[mid:], by_key, ascending, value_index)

        return self._merge(left, right, by_key, ascending, value_index)

    def _merge(self, left, right, by_key, ascending, value_index):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            # Determine the comparison key based on 'by_key'
            left_value = left[i][0] if by_key else left[i][1][value_index]
            right_value = right[j][0] if by_key else right[j][1][value_index]

            # Convert values to numeric types before comparison
            left_value = float(left_value) if isinstance(left_value, (int, float, str)) else left_value
            right_value = float(right_value) if isinstance(right_value, (int, float, str)) else right_value

            # Perform comparison based on the specified order (ascending or descending)
            if (left_value < right_value) if ascending else (left_value > right_value):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result
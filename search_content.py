
# Function that checks the search entry and compares it with the movie data to find a match
def search_movie_file(entry, format):
    def read_tsv_file(filename, title):
        data_dict = {}
        i = -1
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                columns = line.strip().split('\t')
                if len(columns) >= 3:
                    value_to_compare = columns[2].lower()  # Convert to lowercase for input validation
                    if value_to_compare == title:
                        if format == 1:
                            if columns[1] == "movie":
                                i = i + 1
                                data_dict.setdefault(i, []).append(line.strip().split('\t'))  # Save Entire Row
                        elif format == 2:
                            if columns[1] == "tvSeries":
                                i = i + 1
                                data_dict.setdefault(i, []).append(line.strip().split('\t'))  # Save Entire Row

        return data_dict , len(data_dict)
    # Checks if there are movie titles that are not an exact match but contains the searched value and returns the rows
    # that contain it in a dictionary
    def search_tsv_file(filename, partial_string, num):
        data_dict = {}
        with open(filename, 'r', encoding='utf-8') as file:  # Adjust the encoding as needed
            i = num-1
            for line in file:
                columns = line.strip().split('\t')
                if len(columns) >= 3:
                    if partial_string.lower() in columns[2].lower():  # Check if partial string is in the third column
                        if partial_string.lower() != columns[2].lower():
                            if format == 1:
                                if columns[1] == "movie":
                                    i = i + 1
                                    data_dict.setdefault(i, []).append(line.strip().split('\t'))  # Save Entire Row
                            elif format == 2:
                                if columns[1] == "tvSeries":
                                    i = i + 1
                                    data_dict.setdefault(i, []).append(line.strip().split('\t'))  # Save Entire Row

        return data_dict

    search_key = entry.lower()
    exact_match_data, num = read_tsv_file('full_data.tsv', search_key)


    if len(search_key) >3:
        partial_match_data = search_tsv_file('full_data.tsv', search_key, num)
        combined_dict = {**exact_match_data, **partial_match_data}
        return combined_dict
    else:
        return exact_match_data
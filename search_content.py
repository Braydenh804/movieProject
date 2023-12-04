
# Function that checks the search entry and compares it with the movie data to find a match
def search_movie_file(entry, format):
    def read_tsv_file(filename, title):
        movie_data_dict = {}
        tv_data_dict = {}
        i = 0
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                columns = line.strip().split('\t')
                if len(columns) >= 3:
                    value_to_compare = columns[2].lower()  # Convert to lowercase for case-insensitive comparison
                    if value_to_compare == title:
                        i = i-1
                        if columns[1] == "movie":
                            movie_data_dict.setdefault(i, []).append(line.strip().split('\t'))  # Save Entire Row
                        elif columns[1] == "tvSeries":
                            tv_data_dict.setdefault(i, []).append(line.strip().split('\t'))  # Save Entire Row
        if format == 1:
            return movie_data_dict
        elif format == 2:
            return tv_data_dict
    # Checks if there are movie titles that are not an exact match but contains the searched value and returns the rows
    # that contain it in a dictionary
    def search_tsv_file(filename, partial_string):
        movie_data_dict = {}
        tv_data_dict = {}
        with open(filename, 'r', encoding='utf-8') as file:  # Adjust the encoding as needed
            i = -1
            for line in file:
                columns = line.strip().split('\t')
                if len(columns) >= 3:
                    if partial_string.lower() in columns[2].lower():  # Check if partial string is in the third column
                        if partial_string.lower() != columns[2].lower():
                            i = i + 1
                            if columns[1] == "movie":
                                movie_data_dict.setdefault(i, []).append(line.strip().split('\t'))  # Save Entire Row
                            elif columns[1] == "tvSeries":
                                tv_data_dict.setdefault(i, []).append(line.strip().split('\t'))  # Save Entire Row
        if format == 1:
            return movie_data_dict
        elif format == 2:
            return tv_data_dict

    search_key = entry.lower()
    exact_match_data = read_tsv_file('output_file.tsv', search_key)


    if len(search_key) >3:
        partial_match_data = search_tsv_file('output_file.tsv', search_key)
        combined_dict = {**exact_match_data, **partial_match_data}
        # Print the sorted combined dictionary
        for key, values in combined_dict.items():
            print(f"{key}: {values}")
        return combined_dict
    else:
        for key, values in exact_match_data.items():
            print(f"{key}: {values}")
        return exact_match_data
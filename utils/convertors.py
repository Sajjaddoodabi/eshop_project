def group_list(custom_list, size=4):
    grouped_list = []
    my_range = range(0, len(custom_list), size)

    for i in my_range:
        grouped_list.append(custom_list[i:i + size])

    return grouped_list

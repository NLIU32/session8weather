import statistics
from datetime import datetime


series_titles = ["Maximum temperature (Degree C)", "Minimum temperature (Degree C)", "Rainfall amount (millimetres)"]

def mean(in_series):
    
    valid_values = [x for x in in_series if x is not None]
    return sum(valid_values) / len(valid_values)

def variance(in_series):
    valid_values = [x for x in in_series if x is not None]
    if len(valid_values) == 0:
        return None
    avg = mean(valid_values)
    return sum((x - avg) ** 2 for x in valid_values) / len(valid_values)

def standard_deviation(in_series):
    var_result = variance(in_series)
    std_result = var_result ** 0.5
    return std_result
    val = variance(in_series)
    if val is None:
        return None
    else:
        std_result = val ** 0.5
        return std_result

def filter_series(year_series, month_series, day_series, data_series, max_date=None, min_date=None):
    filtered = []
    for y,m, d, value in zip(year_series,
                            month_series,
                            day_series,
                            data_series):
          current = (y, m, d)
          if min_date and current < min_date:
            continue
    
          if max_date and current > max_date:
            continue
    
          filtered.append(value)
    return filtered

def interquartile_range(in_series):
    data = sorted([x for x in in_series if x is not None])
    mid = len(data) // 2

    if len(data) % 2 == 0:
        lower_half = data[:mid]
        upper_half = data[mid:]
    else:
        lower_half = data[:mid]
        upper_half = data[mid + 1:]

    q1 = statistics.median(lower_half)
    q3 = statistics.median(upper_half)

    return q3 - q1

def range_(in_series):
    data = sorted([x for x in in_series if x is not None])
    if len(data) == 0:
        return None
    return data[-1] - data[0]
    range_sort = list(sorted(in_series))
    range_result = range_sort[-1] - range_sort[0]
    return range_result

def read_csv(file,default_value=None):
    data_table = {}
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip().split(',') for line in lines]
    for i in range(1,len(lines[0])):
        conversion = datetime.fromisoformat if (lines[0][i]=='Date') else float
        data_table[lines[0][i]] = \
            [default_value if (len(line[i]) == 0) else conversion(line[i]) for line in lines[1:]]
    return data_table

def get_user_choice(options):
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    choice = input("Enter the number of your choice: ")
    if choice.lower() == 'exit':
        return None
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
        print("Invalid choice. Please try again.")
        return get_user_choice(options)
    choice = int(choice) - 1
    return options[choice]

def menu(data_table):
    print("Select a data series:")
    choice = get_user_choice(series_titles)
    data = data_table[choice]
    print(
        f"Mean: {mean(data)}, "
        f"Variance: {variance(data)}, "
        f"Standard Deviation: {standard_deviation(data)}, "
        f"Interquartile Range: {interquartile_range(data)}, "
        f"Range: {range_(data)}"
)

if __name__ == "__main__":
    data = read_csv('weather.csv')
    menu(data)
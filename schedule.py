import argparse


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-d', '--days',
                    help='Number of days in the shift cycle',
                    default=7,
                    )
parser.add_argument('-s', '--shifts',
                    help='Number of shifts in a day',
                    default=4,
                    )
parser.add_argument('--col_begin',
                    help='Starting column idx (1-based) representing shift choice',
                    default=2,
                    )
parser.add_argument('-D', '--delimiter',
                    help='Delimiter in the input csv file',
                    default=',',
                    )
parser.add_argument('--selected_symbol',
                    help='Symbol representing the corresponding shift is selected',
                    default='1',
                    )
parser.add_argument('-i', '--input',
                    help='Input file',
                    default='',
                    )
parser.add_argument('-o', '--output',
                    help='Output file',
                    default='',
                    )
args = parser.parse_args()


days = int(args.days)
shifts = int(args.shifts)
col_begin = int(args.col_begin)
col_end = col_begin + days * shifts - 1
input_delim = args.delimiter
output_delim = '\t'
selected_symbol = args.selected_symbol
input_file = args.input
output_file = args.output


def calc_schedule(input, schedule):
    shift_max_size = []
    for i in range(shifts):
        shift_max_size.append(0)

    for day in range(days):
        schedule.append([])

    for day in range(days):
        for shift in range(shifts):
            schedule[day].append([])

    while True:
        line = input.readline()
        if line == '':
            break

        name = line.strip().split(input_delim)[0]
        selection = line.strip().split(input_delim)[col_begin-1:col_end]
        for idx, a in enumerate(selection):
            if a == selected_symbol:
                day = idx // shifts
                shift = idx % shifts
                schedule[day][shift].append(name)

    return shift_max_size

if __name__ == '__main__':

    
    schedule = []

    with open(input_file, 'r', encoding='utf-8-sig') as input:
        shift_max_size = calc_schedule(input, schedule)

    # find maximum shift size (to format printing)
    for shift in range(shifts):
        for day in range(days):
            if len(schedule[day][shift]) > shift_max_size[shift]:
                shift_max_size[shift] = len(schedule[day][shift])


    output = open(output_file, 'w', encoding='utf-8-sig')
    # print
    week = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    output.write('\t' + '\t'.join(week) + '\n')
    for shift in range(shifts):
        for row_idx in range(shift_max_size[shift]):
            row = f'{shift+1}\t'
            for day in range(days):
                if row_idx < len(schedule[day][shift]):
                    row += f'{schedule[day][shift][row_idx]}\t'
                else:
                    row += '\t'
            row += '\n'
            output.write(row)

    input.close()
    output.close()
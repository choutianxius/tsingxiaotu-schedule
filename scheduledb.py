'''
把排班表处理成数据库内储存形式
'''
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
parser.add_argument('--shift_strings',
                    help='String representation of each shift in a day delimited by comma.',
                    default='A,B,C,D',
                    )
parser.add_argument('-m','--max_shift_sizes',
                    help='Max shift sizes in a day delimited by comma (leader included).',
                    default='7,8,9,8',
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

NUM_DAYS = args.days
NUM_SHIFTS = args.shifts
SHIFT_STRINGS = str(args.shift_strings).strip().split(',')
MAX_SHIFT_SIZES = str(args.max_shift_sizes).strip().split(',')
MAX_SHIFT_SIZES = [int(x) for x in MAX_SHIFT_SIZES]

input_file = args.input
output_file = args.output


class DayShift:

    def __init__(
        self,
        day_idx = 0,
        shift_idx: int = 0,
        mem_num: int = 0,
        has_leader: int = 0,
        leader_name: str = '',
        leader_studentNum: str = '',
        member: list[str] = []
    ) -> None:
        self.day_idx = day_idx
        self.shift_idx = shift_idx
        self.id = shift_idx + NUM_SHIFTS * day_idx + 1
        self.theClass = str(day_idx+1) + str(SHIFT_STRINGS[shift_idx])
        self.mem_num = mem_num
        self.has_leader = has_leader
        self.leader_name = leader_name
        self.leader_studentNum = leader_studentNum
        self.member = list(member)
        self.max_num = MAX_SHIFT_SIZES[shift_idx]

    def add_member(self, name: str) -> None:
        if str == '':
            raise Exception('Do not add empty member')
        else:
            self.member.append(name)
            self.mem_num += 1

    def to_string(self) -> str:
        fields = [
            self.id,
            self.theClass,
            self.mem_num,
            self.has_leader,
            self.leader_name,
            self.leader_studentNum,
            ' '.join(self.member),
            self.max_num
        ]
        fields = [str(x) for x in fields]
        return(','.join(fields))

def calc_lino(shift_idx, idx):
    return sum(MAX_SHIFT_SIZES[:shift_idx]) + idx


with open(input_file, mode='r', encoding='utf-8') as f:
    input = f.readlines()
input = [line.strip().split(',') for line in input if line != '']

data = {}

for shift_idx in range(NUM_SHIFTS):
    for idx in range(MAX_SHIFT_SIZES[shift_idx]):
        for day_idx in range(NUM_DAYS):
            id = shift_idx + NUM_SHIFTS * day_idx + 1
            lino = calc_lino(shift_idx, idx)
            name = input[lino][day_idx]
            if idx == 0: # 班次内第一个队员是班负
                data[id] = DayShift(
                    day_idx=day_idx,
                    shift_idx=shift_idx,
                    has_leader = 1,
                    leader_name = name,
                )
            elif name != '': # 跳过空单元格
                data[id].add_member(name)

with open(output_file, mode='w', encoding='utf-8') as output:
    for i in range(NUM_DAYS * NUM_SHIFTS):
        line = data[i+1].to_string()
        output.write(line+'\n')

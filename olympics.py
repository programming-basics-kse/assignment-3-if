import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file',type=str, help='Введіть назву файлу з якого програма буде брати дані')
parser.add_argument('-medals',nargs=2 )
parser.add_argument('-total', help='Enter the year' )
# parser.add_argument('country',type=str, help='Введіть назву країни або її код')
# parser.add_argument('year', type=str, help='Введіть рік проведення олімпіади')
parser.add_argument('-o','--output', help="Введіть '-o' та назву файлу, в який хочете вивести результати")
args = parser.parse_args()


with open('olympic.tsv', 'r') as file:
    line = file.readline()
    headers = line.strip('\n').split('\t')
    lines=[]
    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip('\n').split('\t')
        lines.append(line)


country=headers.index('Team')
con_code=headers.index('NOC')
medal=headers.index('Medal')
discipline=headers.index('Event')
name = headers.index('Name')
year=headers.index('Year')


def valid():
    contr_in = args.medals[0]
    year_in = args.medals[1]
    contries = set()
    codes_contr = set()
    years = set()

    for line in lines:
        contries.add(line[country])
        codes_contr.add(line[con_code])
        years.add(line[year])

    if contr_in not in contries and contr_in not in codes_contr:
        print("country not found")
        exit()
    if year_in not in years:
        print("Olympiad wasn't held that year")
        exit()
res_lst=[]
count=0

def medals():
    contr_in = args.medals[0]
    year_in = args.medals[1]
    res_lst = []
    count = 0
    medals = {'Gold': 0,
              'Silver': 0,
              'Bronze': 0}
    for line in lines:
        if count >= 10:
            break
        elif year_in == line[year] and (contr_in == line[con_code] or contr_in == line[country]):
            if contr_in == line[country]:
                output = f"{line[name]}-{line[discipline]}-{line[medal]}"
                if line[medal] in medals:
                    medals[line[medal]]+=1
                res_lst.append(output)
                print(output)
                count += 1
            elif contr_in == line[con_code]:
                output = f"{line[name]}-{line[discipline]}-{line[medal]}"
                if line[medal] in medals:
                    medals[line[medal]]+=1
                res_lst.append(output)
                print(output)
                count += 1



    outcome_medals = f"Gold - {medals['Gold']}, Silver - {medals['Silver']}, Bronze - {medals['Bronze']}"
    print(outcome_medals)

    if args.output:
        with open(args.output, 'a') as output_file:
            for s in res_lst:
                output_file.write(f"{s}\n")
            output_file.write(outcome_medals)
            output_file.write("\n")
            output_file.write("\n")

    if args.output:
        print('result recorded')
total={}
def total_func():
    for line in lines:
        if args.total==line[year]:
            if line[medal]=='Gold':
                if line[country] in total:
                    total[line[country]]['Gold']+=1
                elif line[country] not in total:
                    total[line[country]] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
                    total[line[country]]['Gold'] = 1
            elif line[medal] == 'Silver':
                if line[country] in total:
                    total[line[country]]['Silver']+=1
                elif line[country] not in total:
                    total[line[country]] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
                    total[line[country]]['Silver'] = 1
            elif line[medal]=='Bronze':
                if line[country] in total:
                    total[line[country]]['Bronze']+=1
                elif line[country] not in total:
                    total[line[country]] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
                    total[line[country]]['Bronze'] = 1
    for i in total:
        print(f"{i} - Gold {total[i]['Gold']} - Silver {total[i]['Silver']} - Bronze {total[i]['Bronze']}")



if args.medals:
    valid()
    medals()


if args.total:
    total_func()

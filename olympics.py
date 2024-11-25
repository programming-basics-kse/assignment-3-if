import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file',type=str, help='Введіть назву файлу з якого програма буде брати дані')
parser.add_argument('-medals',nargs=2 )
parser.add_argument('-total', help='Enter the year' )
parser.add_argument("-t","--top", help="Введіть групу серед якої хочете дізнатись топів(M-men, F-women, 1 for 18-25 years, 2 for 25-35 years, 3 for 35-50 years, 5 for 50+ years) у форматі -- top 'M F 1 2'")
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
sex=headers.index('Sex')
age=headers.index('Age')

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
total={}

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


sexes=[]
ages={'1':range(18,25),
      '2':range(25,35),
      '3':range(35,50),
      '5':range(50,120)}
ranges=[]
participants={}
age_participates_f={range(18, 25): {'Olesya Nikolayevna Zykina': [2, 19, 'F']},
                    range(25, 35): {'Julia Zwehl': [1, 28, 'F']},
                    range(35, 50): {'Ellina Aleksandrovna Zvereva (Kisheyeva-)': [2, 35, 'F']},
                    range(50, 120): {'Emily Woodruff (Smiley-)': [1, 58, 'F']}}

age_participates_m={range(18, 25): {'Krzysztof Zwoliski': [1, 21, 'M']},
                    range(25, 35): {'Bogusaw Zych': [1, 28, 'M']},
                    range(35, 50): {'Bla Zulawszky': [1, 38, 'M']},
                    range(50, 120): {'Mahonri Mackintosh Young': [1, 54, 'M']}}

def top_func():
    #визначаємо потрібні групи учасників
    #шукаємо людинку з найбільшою к-тю медалей

    for i in args.top:
        if i is i.isalpha():
            sexes.append(i)
        elif i is i.isnumeric():
            ranges.append(i)
    for i in args.top.split(" "):
        if i in ages:
            ranges.append(i)
        elif i =='F' or i == 'M':
            sexes.append(i)

    if len(ranges)==0:
        print("You have put wrong age")
        exit()
    if len(sexes)==0:
        print("You have put wrong sex")
        exit()
    for line in lines:
        if line[medal]!='NA':
            if line[name] in participants:
                participants[line[name]][0]+=1
            elif line[name] not in participants and line[age]!="NA":
                participants[line[name]] = [0,int(line[age]),line[sex]]
                participants[line[name]][0] = 1

    for k in participants:
        if participants[k][2]=='F':
            for i in age_participates_f:
                for g in age_participates_f[i]:
                    if participants[k][1] in i and participants[k][0]>age_participates_f[i][g][0]:
                        age_participates_f[i]={k:participants[k]}
        elif participants[k][2]=='M':
            for i in age_participates_m:
                for g in age_participates_m[i]:
                    if participants[k][1] in i and participants[k][0] > age_participates_m[i][g][0]:
                        age_participates_m[i] = {k: participants[k]}

    for i in sexes:
        if i=='F':
            for j in ranges:
                age_category= str(ages[j]).replace('range','').replace(",", " до")
                for s in age_participates_f[ages[j]]:
                    print(f"У віковій категорії - {age_category} серед жінок топом є {s}, що здобула {age_participates_f[ages[j]][s][0]} медалей до віку {age_participates_f[ages[j]][s][1]} років ")

        elif i == 'M':
            for j in ranges:
                age_category= str(ages[j]).replace('range','').replace(",", " до")
                for s in age_participates_m[ages[j]]:
                    print(f"У віковій категорії - {age_category} серед чоловіків топом є {s}, що здобув {age_participates_m[ages[j]][s][0]} медалей до віку {age_participates_m[ages[j]][s][1]} років ")





if args.medals:
    valid()
    medals()


if args.total:
    total_func()

if args.top:
    top_func()
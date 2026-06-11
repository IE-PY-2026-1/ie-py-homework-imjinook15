# 파일이름 :
# 작 성 자 :
my_name = " "
team = " "
time = 0
min_fee = 0
base_fee = 0
max_fee = 0
rate = 0.0
num = 0
names = []
member_data = []
total = 0

def calculate_fee(status, mins, name):
    global max_fee, base_fee, min_fee, rate, my_name

    if status == 2:
        print(f'무임승차 적발! {name}님의 결석으로 오늘 팀플은 파토났습니다!')
        print(f'{name}님 에게 최대벌금 {max_fee}원을 부과하고 남은 정산을 중단합니다.')
        return max_fee, '무단결석', True
    
    elif status == 1:
        if mins == 0:
            print(f'정상 출석하여 벌금 계산을 건너뜁니다.')
            return 0, '정상출석', False
        
        if mins > 0:
            if mins > 0 and mins < 10:
                calc_fee = base_fee + (mins*min_fee)
                fee = int (calc_fee)
                print(f"지각하셨습니다. {name}님의 벌금: {fee}원 입니다. ")
                return fee, '단순지각', False
            else:
                calc_fee = (base_fee + (mins*min_fee)*rate)
                fee = int(calc_fee)
                print(f'10분이상 지각으로 가중치가 부과됩니다. {name}님의 벌금: {fee}원 입니다.')
                return fee, '가중지각', False
        
    else:
        fee = 10000
        print(f'[경고] 1, 2번 이외의 숫자를 입력했습니다')
        print(f'장난친 대가로 해당 조원 대신 작성자 {my_name}님에게 [진행 방해죄]가 적용되어 {fee}원의 벌금을 즉시 부과합니다')
        return fee, '진행방해', False
    
def input_member_status():
    global time, names, member_data, total

    print('\n---팀원 출석 상태 입력---')
    for name in names:
        while True:
            try:
                status = int(input(f'\n 조원 {name}님의 상태를 숫자로 입력해주세요(1:출석/지각, 2:무단결석):'))
                break
            except ValueError:
                print('[오류] 상태는 숫자로만 입력해주세요!')

        if status == 2:
            fee, status_str, is_break = calculate_fee(status, 0, name)
            member_data.append([name, status_str,0,fee])
            total += fee
            if is_break:
                break
        
        elif status == 1:
            while True:
                try:
                    mins = int(input(f'{name}님의 지각시간(분)을 입력하세요. (정각 도착은 {time}시): '))
                    break
                except ValueError:
                    print('[오류] 지각 시간은 숫자로만 입력해주세요!')
            fee, status_str, is_break = calculate_fee(status, mins, name)
            member_data.append([name, status_str, mins, fee])
            total += fee
        
        else:
            fee, status_str, is_break = calculate_fee(status, 0, name)
            member_data.append([my_name, status_str, 0, fee])
            total += fee

def view_data():
    global total, team, member_data
    print('\n========================================')
    print(f'     [{team}] 조별과제 벌금 정산 결과')
    print('========================================')
    print(f"{'이름':^10}|{'상태':^10}|{'지각(분)':^10}|{'벌금(원)':^10}")
    print('-'*55)

    if not member_data:
        print(f"{'입력된 데이터가 없습니다.':^55}")
    else:
        for row in member_data:
            for item in row:
                print(f"{str(item):^11}", end = ' | ')
            print()
    print('========================================')
    print(f'최종 모인 회식비: {total}원')

def save_data():
    global team, member_data, total

    file_name = f'{team}_벌금정산내역.txt'
    try:
        with open(file_name, 'w', encoding = 'utf-8')as f:
            f.write(f'[{team}] 조별과제 벌금 정산 결과\n')
            f.write('='*40 + '\n')
            for row in member_data:
                f.write(f'이름: {row[0]}, 상태: {row[1]}, 지각: {row[2]}분, 벌금: {row[3]}원\n')
            f.write('='*40 + '\n')    
            f.write(f'총 모인 회식비: {total}원\n')
        print(f"\n[성공] 데이터가 '{file_name}' 파일로 안전하게 저장되었습니다.")
    except IOError:
        print(f'\n[오류] 파일 저장 중 문제가 발생했습니다.')
            
            

def analyze_data():
    global member_data
    if not member_data:
        return 0, ""
    
    max_fee_row = member_data[0]

    for row in member_data:
        if row[3] > max_fee_row[3]:
            max_fee_row = row
    
    return max_fee_row[3], max_fee_row[0]

def main():
    global my_name, team, time, min_fee, base_fee, max_fee, rate, num, names

    print('=== 지옥의 팀플 벌금 관리기 시작 ===')
    try:
        my_name = input('본인(기록자)의 이름을 먼저 입력하세요:')
        team = input("팀플 조 이름을 입력하세요: ")
        time = int(input('회의 시작시간을 입력하세요 (예: 1 or 18과 같이 정각만 가능): '))
        min_fee = int(input('1분당 지각 벌금액을 입력하세요 (예: 500): '))
        base_fee = int(input('기본 지각 벌금액을 입력하세요 (예: 2000): '))
        max_fee = int(input('무단결석 시 부과할 최대 벌금액을 입력하세요 (예: 500000): '))
        rate = float(input('이번 주 지각비 가중치를 입력하세요 (예: 1.5): '))
        num = int(input('본인을 포함한 조원이 총 몇명 인가요 (예: 4): '))
    except ValueError:
        print('\n[오류] 숫자입력란에 문자가 입력되었습니다. 프로그램을 다시 실행해주세요.')
        return

    print(f'\n[{team}]팀의 조원 등록을 시작합니다.')
    names = []
    names.append(my_name)
    for i in range(num-1):
        name = input(f'{i+2}번째 조원 이름을 입력하세요:')
        names.insert(0, name)
    cnt = len(names)
    print(f'\n 총 {cnt}명의 조원이 등록되었습니다.')
    
    while True:
        print('\n' + '='*40)
        print('     지옥의 팀플 관리기 메인메뉴')
        print('='*40)
        print(' 1. 입력(팀원 지각/결석 상태 입력 및 계산)')
        print(' 2. 조회 (현재까지 모인 회식비 확인)')
        print(' 3. 분석 (가장 비싼 벌금 내역 확인)')
        print(' 4. 저장 (파일로 데이터 내보내기)')
        print(' 5. 종료')
        
        choice = input('원하는 메뉴 번호를 입력하세요: ')

        if choice == '1':
            input_member_status()
            print('입력 및 계산이 완료되었습니다.')
        elif choice == '2':
            view_data()
        elif choice == '3':
            if not member_data:
                print('아직 벌금 내역이 없습니다. 먼저 1번 메뉴를 통해 출석 상태를 입력해주세요.')
            else:
                real_max_fee, max_name = analyze_data()
                print(f'가장 비싼 벌금을 낸 사람: {max_name}님 {real_max_fee}원')
                print('='*40)
        elif choice == '4':
            if not member_data:
                print('저장할 데이터가 없습니다. 먼저 1번 메뉴를 진행해주세요.')
            else:
                save_data()
        elif choice == '5':
            print('프로그램을 종료하기 전 데이터를 자동 저장합니다...')
            if member_data:
                save_data()
            print('프로그램을 종료합니다')
            break
        else:
            print('잘못된 입력입니다. 1~5 사이의 숫자를 입력해주세요.')

if __name__ == '__main__':
    main()
    

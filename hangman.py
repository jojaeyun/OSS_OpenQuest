import sys
import random as r
import time
import hangman_words

def c_alps(word):
    letters = {ch for ch in word}
    return len(letters)

def main():
    inplst = []
    c_word = r.choice(hangman_words.word_list)    # 랜덤 선택
    alp_num = c_alps(c_word)    # 해당 단어에 쓰인 알파벳 종류의 개수
    count = 0
    t = 10   # 가능한 횟수
    print("기회는 총 {}번\n".format(t))
    time.sleep(1) # 게임 실행 속도를 조절하기 위해 사용

    while count <= t:
        print("\n단어: ",end="")
        s = True
        for i in c_word:
            if i in inplst:
                print(i,end=" ")
            else:
                print("_",end=" ")
                s = False
        time.sleep(1)

        if s == True: # 남은 기회가 있는데 알파벳을 전부 맞추었으면 성공
                print("\n정답입니다")
                break
        
        if t-count != 0:
            print("\n\n남은 기회: {}번".format(t-count))
        else: # 기회 소진시 
            if s == True: # 기회를 다 썼는데 알파벳도 다 맞췄으면 축하해주고 탈출
                print("\n정답입니다")
            break
       
        time.sleep(1)
        # 알파벳 입력 & 잘못된 입력을 받았을 경우
        print("\n알파벳 입력: ",end="")
        alp = sys.stdin.readline().rstrip()
        if not alp.isalpha() or not alp.isascii():
            print("\nError: 알파벳 입력되지 않음\n")
            time.sleep(0.5)
            continue
        elif len(alp) > 1:
            print("\nError: 두 개 이상의 입력 확인\n")
            time.sleep(0.5)
            continue
        
        alp = alp.lower()
        if alp not in c_word:
            print("\n이 알파벳은 존재하지 않습니다\n")
        else:
            if alp not in inplst:
                print("\n이 알파벳은 존재합니다\n") 
                inplst.append(alp)
                alp_num -= 1
            else: # 이미 맞춘 알파벳을 다시 입력한다면
                print("\n이미 맞춘 알파벳입니다\n")
                continue
        count += 1
        time.sleep(1)

        if (t-count) < alp_num: # 맞춰야 할 알파벳이 남은 기회보다 많아지면 조기종료
            print("\n더이상 정답을 맞출 수 없어 조기종료합니다")
            break

        if alp_num == 0: # 알파벳을 다 맞춰 더이상 맞출 알파벳이 없으면 아래 문장은 불필요하다.
            continue
    if s == False:
        print("\n정답: {}".format(c_word))
        print("\n아쉽게도 성공하지 못하였습니다\n")
 
 # 실행
main()

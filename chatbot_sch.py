import pandas as pd
import os


# 레벤슈타인 거리 계산 함수 정의
def calc_distance(a, b):
    ''' 두 문자열 a, b 간의 레벤슈타인 거리(편집 거리)를 계산 '''
    if a == b:
        return 0
    a_len = len(a)
    b_len = len(b)
    if a == "":
        return b_len
    if b == "":
        return a_len
    
    # 2차원 matrix 초기화 (크기: (a_len+1) x (b_len+1))
    matrix = [[] for i in range(a_len + 1)]
    for i in range(a_len + 1):
        matrix[i] = [0 for j in range(b_len + 1)]
    
    # 첫 번째 행과 열 초기값 설정 (빈 문자열 비교를 위한 처리)
    for i in range(a_len + 1):
        matrix[i][0] = i
    for j in range(b_len + 1):
        matrix[0][j] = j

    # 나머지 matrix 채우기 (동적 프로그래밍 활용)
    for i in range(1, a_len + 1):
        ac = a[i - 1]
        for j in range(1, b_len + 1):
            bc = b[j - 1]
            cost = 0 if ac == bc else 1
            matrix[i][j] = min([
                matrix[i - 1][j] + 1,      # 삭제
                matrix[i][j - 1] + 1,      # 삽입
                matrix[i - 1][j - 1] + cost  # 교체
            ])
    return matrix[a_len][b_len]

# 레벤슈타인 거리 기반 챗봇 클래스 정의
class LevenshteinChatBot:
    def __init__(self, filepath):
        # 학습 데이터를 로드
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        ''' CSV 파일에서 Q(질문), A(답변) 데이터를 로드 '''
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열 리스트화
        answers = data['A'].tolist()    # 답변열 리스트화
        return questions, answers

    def find_best_answer(self, input_sentence):
        ''' 입력 문장과 가장 가까운 질문을 찾아 해당 답변 반환 '''
        # 각 질문과 입력 문장 간의 레벤슈타인 거리 계산
        distances = [calc_distance(input_sentence, question) for question in self.questions]

        # 가장 거리가 작은 질문(가장 유사한 질문)의 인덱스를 찾음
        best_match_index = distances.index(min(distances))

        # 해당 인덱스의 답변 반환
        return self.answers[best_match_index]

# 현재 파이썬 파일(chatbot_sch.py)이 있는 디렉토리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# CSV 파일 경로 (현재 디렉토리 + ChatbotData.csv)
filepath = os.path.join(current_dir, 'ChatbotData.csv')

# 챗봇 인스턴스 생성
chatbot = LevenshteinChatBot(filepath)

# 대화 루프 실행 ('종료' 입력 시 종료)
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        print("Chatbot: 대화를 종료합니다.")
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
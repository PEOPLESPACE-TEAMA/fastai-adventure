from fastai.vision.all import *
from fastai.vision.widgets import *
import pathlib
import platform


'''
삽질 해서 알아낸 에러 깔끔하게 fastai 설치하는 방법
먼저 https://pytorch.org/get-started/locally/ 여기에서 자기 시스템에 맞는 파이토치를 먼저 설치
다음에 pip install fastai==2.2.5 설치
완벽
'''

'''
윈도우의 경우 모델을 그냥 로드 할려는 경우에 경로 문제가 있음
플랫폼이 윈도우인 경우하고 아닌경우하고 둘 나눠서 경로를 지정하고 
모델을 로딩 해야함
근데 제가 윈도우라서 일단 윈도우는 테스트된 상태인데 다른 환경에서도 잘 되겠죠 뭐..
'''

'''
모델과 모델에 넣을 사진의 경로를 mamge.py가 있는 곳을 기준으로 경로를 잡음 
'''

#패스 설정 모델은 그냥 임시로 아무거나 넣은거임 나중에 바꿔야함
path = Path("./resnet18.pkl") #모델 경로를 mamge.py 하고 같은 디렉토리에 있어야함
assert path.exists()


model = None
if platform.system() =='Windows':       
    tmp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath
    model = load_learner(path)
    pathlib.PosixPath = tmp
else:
    model = load_learner(path)

#print(type(model))

'''
이걸 def 해서 함수안에 넣을 수도 있는데 그렇게 하면 예측 한번 할때마다
모델을 불러와야 해서 시간이 오래 걸릴것이다. 그래서 밖으로 빼놔서 처음 한번 임포트 할때 모델을 불러옴.
'''


def predict(img):
    '''
    이미지 경로를 인풋으로 넣으면 됨
    예측 결과, 예측결과 레이블의 인덱스, 확률을 리턴 받음 
    pred: 레이블 , probs[pred_idx]: 확률
    '''
    pred,pred_idx,probs = model.predict(img)
    return pred, pred_idx, probs


def getLabels():
    '''
    이 모델의 라벨들을 리스트로 반환
    '''
    return model.dls.vocab
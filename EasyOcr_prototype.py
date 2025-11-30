import easyocr
import cv2
import warnings
import numpy as np  # <-- NumPy 임포트가 필요합니다!

# (경고 메시지 무시)
warnings.filterwarnings('ignore')

# --- 1. OpenCV 전처리 단계 (수정됨) ---
try:
    # 1. 'r'을 붙여 raw string으로 경로를 지정 (SyntaxError 해결)
    image_path = r'C:\Users\hwko3\OneDrive\바탕 화면\고희원\숭실대\1학년\2) 오픈소스설계\프로젝트\test_영수증.jpg'
    
    # 2. np.fromfile과 cv2.imdecode로 한글 경로 문제 해결
    n = np.fromfile(image_path, np.uint8)
    image = cv2.imdecode(n, cv2.IMREAD_COLOR)

    if image is None:
        raise Exception("이미지 파일을 불러올 수 없습니다. 경로를 확인하세요.")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # 어댑티브 스레시홀딩 적용
    binary_image = cv2.adaptiveThreshold(
        blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

except Exception as e:
    print(f"오류: 이미지 처리 중 문제가 발생했습니다. {e}")
    exit()

# --- 2. EasyOCR 텍스트 추출 단계 ---
# (이하 코드는 동일)

print("EasyOCR 리더를 초기화합니다 (모델 다운로드에 시간이 걸릴 수 있습니다)...")
reader = easyocr.Reader(['ko', 'en'])

print("텍스트 인식을 시작합니다...")
results = reader.readtext(binary_image)

# --- 3. 결과 출력 ---
print("\n--- EasyOCR 인식 결과 ---")
if not results:
    print("인식된 텍스트가 없습니다.")
else:
    for (bbox, text, prob) in results:
        print(f"인식된 텍스트: {text}  (정확도: {prob:.2f})")
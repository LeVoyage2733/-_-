# OpenCV를 통해 전처리된 영수증 jpg를 tesseract를 통해 ocr하기

import cv2
import numpy as np
import pytesseract  # Tesseract 모듈 임포트

# --- 0. Tesseract 설치 경로 설정 (필수!) ---
# Tesseract OCR이 설치된 정확한 경로를 지정해야 합니다.
# (기본 설치 경로: C:\Program Files\Tesseract-OCR\tesseract.exe)
# 
# [중요] 이 경로가 잘못되면 'TesseractNotFoundError' 오류가 발생합니다.
# 본인의 설치 경로에 맞게 수정해주세요.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- 1. OpenCV 전처리 단계 (이전과 동일) ---
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
    
    # 어댑티브 스레시홀딩 적용 (Tesseract는 깨끗한 이진화 이미지를 선호합니다)
    binary_image = cv2.adaptiveThreshold(
        blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    # cv2.imwrite('preprocessed_for_tesseract.png', binary_image) # 전처리 확인용

except Exception as e:
    print(f"오류: 이미지 처리 중 문제가 발생했습니다. {e}")
    exit()

# --- 2. Tesseract 텍스트 추출 단계 ---
print("Tesseract 텍스트 인식을 시작합니다...")

try:
    # Tesseract가 OCR을 수행할 때 사용할 언어 설정 (한국어+영어)
    # lang='kor+eng'
    
    # Tesseract의 세부 옵션 설정
    # --oem 3: 기본 LSTM 엔진 사용
    # --psm 4: 페이지를 단일 텍스트 컬럼으로 간주 (영수증에 적합할 수 있음)
    # (더 많은 옵션: --psm 6은 단일 블록, 3은 자동)
    custom_config = r'--oem 3 --psm 4'
    
    # OpenCV로 전처리된 이미지를 Tesseract로 바로 전달
    text = pytesseract.image_to_string(
        binary_image, 
        lang='kor+eng', 
        config=custom_config
    )

    # --- 3. 결과 출력 ---
    print("\n--- Tesseract 인식 결과 ---")
    if not text.strip():
        print("인식된 텍스트가 없습니다.")
    else:
        # EasyOCR과 달리 Tesseract는 하나의 긴 문자열로 결과를 반환합니다.
        print(text)

except pytesseract.TesseractNotFoundError:
    print("="*50)
    print(" [중요] 오류: TesseractNotFoundError")
    print(" Tesseract가 시스템에 설치되어 있지 않거나, Python이 Tesseract를 찾지 못했습니다.")
    print(f" 해결책 1: 코드 상단의 'pytesseract.tesseract.tesseract_cmd' 경로가")
    print(f"          (현재 설정: r'{pytesseract.pytesseract.tesseract_cmd}')")
    print(f"          실제 tesseract.exe 파일 위치와 일치하는지 확인하세요.")
    print(" 해결책 2: Tesseract-OCR 프로그램을 설치했는지 확인하세요.")
    print("="*50)
except Exception as e:
    print(f"Tesseract OCR 실행 중 오류가 발생했습니다: {e}")
    print("Tesseract 설치 시 'kor' (한국어)와 'eng' (영어) 언어 팩을 설치했는지 확인하세요.")
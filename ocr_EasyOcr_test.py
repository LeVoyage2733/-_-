import easyocr
import time

# Pytesseract 때 사용한 파일 경로 (이 부분은 그대로 둡니다)
file_path = r'C:\Users\hwko3\OneDrive\바탕 화면\고희원\숭실대\1학년\2) 오픈소스설계\프로젝트\test_영수증.jpg'

print("EasyOCR 엔진을 로드하는 중입니다...")
start_time = time.time()

# 1. OCR 리더기 초기화
reader = easyocr.Reader(['ko', 'en'], gpu=False) 

load_time = time.time() - start_time
print(f"엔진 로드 완료! (소요 시간: {load_time:.2f}초)")

print("OCR을 수행하는 중입니다...")
start_time = time.time()

# ★★★★★★★★★★★ 수정된 부분 ★★★★★★★★★★★
# 파일 경로(file_path) 대신 파일의 바이트(bytes)를 전달합니다.
try:
    # 1. 파일을 '읽기 바이너리(rb)' 모드로 엽니다.
    with open(file_path, "rb") as f:
        image_bytes = f.read()

    # 2. 파일 경로(string) 대신 파일의 내용(bytes)을 전달합니다.
    result = reader.readtext(image_bytes)
    
    ocr_time = time.time() - start_time
    print(f"OCR 완료! (소요 시간: {ocr_time:.2f}초)")

    # 3. 결과 출력
    print("\n--- EasyOCR 결과 ---")
    for (bbox, text, prob) in result:
        print(f"인식된 텍스트: {text} (정확도: {prob:.4f})")
    print("----------------------")

except FileNotFoundError:
    print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"오류 발생: {e}")
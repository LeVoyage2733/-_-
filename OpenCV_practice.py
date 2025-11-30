# 전처리

import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 이미지 불러오기 (영수증 이미지라고 가정)
try:
    image_path = r'C:\Users\hwko3\OneDrive\바탕 화면\고희원\숭실대\1학년\2) 오픈소스설계\프로젝트\test_영수증.jpg'
    
    # 
    # ▼▼▼▼▼ 한글 경로 해결을 위해 이 부분 수정 ▼▼▼▼▼
    #
    # 1. numpy를 사용해 파일을 바이너리로 읽음
    n = np.fromfile(image_path, np.uint8)
    # 2. cv2.imdecode를 사용해 numpy 배열을 이미지로 디코딩
    image = cv2.imdecode(n, cv2.IMREAD_COLOR)
    #
    # ▲▲▲▲▲ 수정 완료 ▲▲▲▲▲
    #

    if image is None:
        print(f"오류: 이미지를 불러올 수 없습니다. 경로를 확인하세요: {image_path}")
    else:
        # 2. 그레이스케일 변환
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 3. 노이즈 제거 (Gaussian Blur)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        # 4. 이진화 (Adaptive Thresholding)
        binary_image = cv2.adaptiveThreshold(
            blurred_image, 
            255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            11, 
            2  
        )

        # 결과 표시 (테스트용)
        plt.figure(figsize=(15, 5))
        
        plt.subplot(1, 3, 1)
        plt.title('Original')
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        plt.subplot(1, 3, 2)
        plt.title('Grayscale')
        plt.imshow(gray_image, cmap='gray')

        plt.subplot(1, 3, 3)
        plt.title('Adaptive Threshold (Result)')
        plt.imshow(binary_image, cmap='gray')
        
        plt.show()

except Exception as e:
    print(f"오류: 이미지를 찾을 수 없거나 처리 중 문제가 발생했습니다. {e}")
import json
import os

# 바운딩 박스의 좌표를 YOLO 형식으로 변환하는 함수
def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = box[0] + box[2]/2.0
    y = box[1] + box[3]/2.0
    w = box[2]
    h = box[3]
    x = round(x * dw, 6)
    w = round(w * dw, 6)
    y = round(y * dh, 6)
    h = round(h * dh, 6)
    return (x, y, w, h)

# 대상 폴더 리스트
folders = ['C1','G1','H1','I1','T1']

# YOLO 클래스에 대응하는 이름 매핑을 카테고리 이름으로 변경
class_names = {
    "건축전기설비작업": 4,
    "고소작업": 5,
    "배전설비작업": 2,
    "변전설비작업": 3,
    "지중송전설비작업": 0,
    "철탑설비작업": 1
}

# 오류가 발생한 JSON 파일명을 담을 리스트
error_files = []

# 'S63_1_DATA3-001' 폴더 내의 각 폴더에 대해
for index, folder in enumerate(folders):
    folder_path = os.path.join('S63_DATA1-001', folder)

    # 각 폴더에 있는 모든 JSON 파일에 대해
    for json_file_name in os.listdir(folder_path):
        if not json_file_name.endswith('.json'):
            continue  # JSON 파일이 아니면 건너뜀

        with open(os.path.join(folder_path, json_file_name), encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                error_files.append(json_file_name)
                continue

        size = [data['images']['width'], data['images']['height']]

        # .txt 파일 생성
        txt_file_name = json_file_name.replace('.json', '.txt')
        txt_file_path = os.path.join(folder_path, txt_file_name)

        with open(txt_file_path, 'w') as tf:
            for ann in data['annotations']:
                try:
                    # "categories" 키가 존재하는지 확인
                    if 'categories' in ann and ann['categories']:
                        if len(ann['categories'][0]) == 2:
                            category_name = ann['categories'][0].get('value')
                        elif len(ann['categories'][0]) == 1:
                            category_name = ann['categories'][0]['작업공정']
                    else:
                        category_name = ann['categories'][0]['value']
                        
                    class_id = class_names.get(category_name)
                    if class_id is None:
                        raise ValueError(f"카테고리 '{category_name}'에 대응하는 클래스 ID가 없습니다.")

                    bbox = ann['bbox']
                    bb = convert(size, bbox)

                    # .txt 파일에 한 줄로 저장
                    line = f"{class_id} {bb[0]} {bb[1]} {bb[2]} {bb[3]}\n"

                    # 디렉토리에 저장
                    tf.write(line)
                except (IndexError, ValueError) as e:
                    error_files.append((json_file_name, str(e)))
                    continue

# 오류가 발생한 JSON 파일명 출력
print("오류가 발생한 파일들:")
for file_name, error_message in error_files:
    print(f"{file_name}: {error_message}")

# 오류가 발생한 파일명과 개수를 텍스트 파일로 저장
output_file_path = "error_files.txt"
with open(output_file_path, 'w') as output_file:
    output_file.write(f"오류가 발생한 파일 개수: {len(error_files)}\n")
    output_file.write("오류가 발생한 파일들:\n")
    for file_name, error_message in error_files:
        output_file.write(f"{file_name}: {error_message}\n")
# txt 파일 복사 후 붙여넣기
import os
import shutil

# 대상 폴더 리스트
folders = ['C1','G1','H1','I1','T1']

# 텍스트를 복사하고자 하는 디렉토리 명시
label_copy_train_dir = os.path.join('.', 'train', 'labels')
label_copy_val_dir = os.path.join('.', 'val', 'labels')
os.makedirs(label_copy_train_dir, exist_ok=True)
os.makedirs(label_copy_val_dir, exist_ok=True)

# 'S63_1_DATA3-001' 폴더 내의 각 폴더에 대해
for folder in folders:
    folder_path = os.path.join('S63_DATA1-001', folder)

    # 대상 폴더 내의 모든 파일에 대해
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 파일 경로
            source_path = os.path.join(root, file)

            # txt 파일만 복사
            if file.lower().endswith('.txt'):
                # 대상 디렉토리에 파일 복사
                destination_path_train = os.path.join(label_copy_train_dir, file)
                destination_path_val = os.path.join(label_copy_val_dir, file)
                try:
                    shutil.copy(source_path, destination_path_train)
                    shutil.copy(source_path, destination_path_val)
                except FileNotFoundError:
                    print(f"Warning: Image not found: {source_path}")
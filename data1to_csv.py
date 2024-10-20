import os
import pandas as pd
from scipy.io import loadmat

# 각 결함 유형을 나타내는 리스트
fault_types = ['내륜결함', '롤러결함', '외륜결함', '정상']
data_frames = []  # 데이터프레임을 저장할 리스트

for fault in fault_types:
    data_dir = fr'C:\Users\medici\901\학습용 데이터1\{fault}'
    all_signals = []
    all_fs = []

    # 폴더 내 모든 .mat 파일을 읽어옴
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.mat'):
            file_path = os.path.join(data_dir, file_name)
            mat_data = loadmat(file_path)
            signal_data = mat_data['signal'].flatten()
            fs = mat_data['fs'][0][0]

            all_signals.append(signal_data)
            all_fs.append(fs)

    # 데이터프레임으로 변환
    df_signals = pd.DataFrame(all_signals)
    df_signals['fs'] = all_fs
    df_signals['fault_type'] = fault  # 결함 유형 추가

    # 리스트에 데이터프레임 추가
    data_frames.append(df_signals)

# 모든 데이터프레임을 하나로 결합
final_df = pd.concat(data_frames, ignore_index=True)

# fault_type을 라벨링
label_mapping = {
    '내륜결함': 1,
    '롤러결함': 2,
    '외륜결함': 3,
    '정상': 0
}

# fault_type 열을 숫자로 변환
final_df['fault_type'] = final_df['fault_type'].replace(label_mapping)

final_df = final_df.drop(columns=['fs'])

final_df.to_csv('learning1_data.csv', index=False, encoding='utf-8-sig')  # index=False로 인덱스 열을 저장하지 않음
"""
위 모듈은 개발자 뭉개구름이 제작하였으며 무단으로 사용할 경우 라이선스 위반에 해당됩니다.
"""

import json

class Module():
    def __init__(self):
        self.module = 'JSON 모듈입니다!'

    def save(self, filename, data):
        print(f'[JSON MODULE] [작업시도] {filename} 파일을 저장중입니다...')
        with open(filename, encoding='utf-8', mode='w') as f:
            json.dump(data, f, sort_keys=True,
                separators=(',',' : '), ensure_ascii=False)        
        print(f'[JSON MODULE] [Success] {filename} 파일을 성공적으로 저장하였습니다!')
        return data

    def open(self, filename):
        print(f'[JSON MODULE] [작업시도] {filename} 파일을 여는중입니다...')
        with open(filename, encoding='utf-8', mode='r') as f:
            data = json.load(f)
        print(f'[JSON MODULE] [Success] {filename} 파일을 성공적으로 열었습니다!')
        return data
        
    def is_vaild(self, filename):
        print(f'[JSON MODULE] [작업시도] {filename} 파일이 있는지 확인하는중입니다...')
        try:
            self.open(filename)
            print(f'[JSON MODULE] [Success] {filename} 파일이 정상적으로 감지되었습니다!')
            return True
        except FileNotFoundError:
            print(f'[JSON MODULE] [Failed] {filename} 파일이 정상적으로 감지하지 못했습니다...')
            return False
        except json.decoder.JSONDecodeError:
            print(f'[JSON MODULE] [Failed] {filename} 파일이 정상적으로 감지하지 못했습니다...')        
            return False
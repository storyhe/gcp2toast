#/usr/bin/python3

from helper.Toast import ToastAuth, ToastContainerService, ToastToken
from helper.Google import GoogleStorageHelper
import options, slack, os

class MoveToast(object):

    def __init__(self):
        self.toast_token = None
        self.storage = GoogleStorageHelper(options.BUCKET_NAME)
        self.toast = ToastAuth()

        token = self.toast.get_token() # 토스트로 토큰을 받음.

        if token.get_token_id() is None:
            slack.to_slack('toast로 부터 인증정보를 수령하지 못하였습니다. 다시 확인해주세요')
            exit

        slack.to_slack('toast로 부터 새로운 인증정보를 받았습니다. {}'.format(token.get_token_id()))
        self.toast_token = token

        self.fetch()

    def fetch(self):
        container = ToastContainerService(self.toast_token.get_token_id())
        print("파일 목록을 가져오는 중입니다.")
        objects = self.storage.lists()
        print(" = = = = = = = = = = = ")

        
        for file_object in objects:

            if self.toast_token.is_token_expired() == True: #토큰이 만료되었다면
                token = self.toast.get_token() # 토스트로 토큰을 받음.

                if token.get_token_id() is None:
                    self.toast_token = token
                    slack.to_slack('토큰 만료로toast로 부터 새로운 인증정보를 받았습니다. {}'.format(self.token.get_token_id()))
                    container = ToastContainerService(self.token.get_token_id())

            filename = file_object.name

            print("[>] {} 파일 업로드".format(filename))
            toastCheck = container.get_object_exists(filename)
            if toastCheck == True:
                print("[X] 이미 업로드 되어있어서 업로드 안함.")
            elif toastCheck == None:
                print("[?] 토스트 응답 에러, 다시 시도해주세요.")
                slack.to_slack('toast로 부터 파일체크에 실패하였습니다. 파일명: {}'.format(filename))
                exit
            elif toastCheck == False: #파일이 없음
                print("[>] GCP STORAGE 에서 파일 다운로드를 시도합니다.")
                filepath = self.storage.get(filename)
                if filepath is not None:
                    print("[>>] 다운로드에 성공하였습니다..: {}".format(filepath))
                    toastUpload = container.upload_file(filename, filepath)
                    if toastUpload == True:
                        print("[>>] 토스트 업로드에 성공하였습니다.")
                        os.remove(filepath)
                    else:
                        slack.to_slack('toast로 업로드에 실패하였습니다. 파일명: {}'.format(filename))
                        exit
                else:
                    print("[{}] 다운로드 실패 하였습니다.")
                    slack.to_slack('GCP부터 부터 파일 다운로드에 실패하였습니다. 파일명: {}'.format(filename))
                    exit

            print("[>>] 종료")        

            # print("[{}] 다운로드 시작..")
            



if __name__ == "__main__":
    MoveToast()
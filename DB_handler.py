import pyrebase
import json


class DBModule:
    def __init__(self):
        with open("./auth/firebaseAuth.json") as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.storage = firebase.storage()
    
    
    # 모바일을 통해 전달받은 firebase storage 경로를 통해 fireabse storage에서 사진 가져오기
    def pull(self, path_cloud):
        mode, uid, filename = path_cloud.split('/')[1:]
        path_dlocal = 'static/downloads/' + mode + '_' + uid + '_' + filename
        self.storage.child(path_cloud).download(path_dlocal)
        return path_dlocal, mode, uid, filename
    
    
    def push(self, mode, uid, filename, path_ulocal, info, summary, error):
        information = {
            "info": info,
            "summary": summary,
            "error": error
        }
        path_on_cloud = "Model/" + mode + "/" + uid + "/" + filename
        self.storage.child(path_on_cloud).put(path_ulocal)
        self.db.child(uid).child(mode).child(filename.split('.')[0]).set(information)
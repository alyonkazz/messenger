import os

from pymongo import MongoClient

HOST_DB = 'localhost'
PORT_DB = 27017


class MongoDB:
    def __init__(self, host_db, port_db):
        my_client = MongoClient(f"mongodb://{host_db}:{port_db}/")
        my_db = my_client["new_test_db"]
        self.my_col = my_db["doctors_collection"]

        self.img_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

        self.fill_db()

    def fill_db(self):
        for i in os.listdir(self.img_dir_path):
            try:
                self.get_image(i)
            except TypeError:
                self.save_image(i, os.path.join(self.img_dir_path, i))

    def save_image(self, img_name, img_path):
        with open(img_path, "rb") as f:
            bytes_data = f.read()

        self.my_col.insert_one({"name": img_name, "image": bytes_data})

    def get_image(self, img_name):
        image_bytes_data = self.my_col.find_one({'name': img_name})['image']

        return image_bytes_data


if __name__ == '__main__':
    # HOST_DB = '192.168.2.8'
    db = MongoDB(HOST_DB, PORT_DB)
    # db.save_image()
    db.get_image('12')
    # db.fill_db()


from library.config import get_absolute_path , data_base_path

if __name__ == "__main__":
    db_path = get_absolute_path('data_base_path')
    print(db_path)
from src.etl import extract, transform, load, url
from src.database import save_to_db

def run():
    r_data = extract(url)
    t_data = transform(r_data)
    df = load(t_data)
    if df is not None:
        try:
            save_to_db(df)
            print("Dataframe saved to Database")
        except Exception as e:
            print(f"Error saving: {e}")

if __name__ == "__main__":
    run()
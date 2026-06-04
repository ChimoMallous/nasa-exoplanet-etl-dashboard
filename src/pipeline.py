from etl import extract, transform, load_to_db, url

def run():
    r_data = extract(url)
    t_data = transform(r_data)
    if t_data is not None:
        try:
            load_to_db(t_data)
            print("Dataframe saved to Database")
        except Exception as e:
            print(f"Error saving: {e}")

if __name__ == "__main__":
    run()
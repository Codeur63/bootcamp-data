from feast import FeatureStore


def get_customer_features(customer_id: str):    
    store = FeatureStore(repo_path="feature_repo")    

    response = store.get_online_features(
        features=["transaction_features:amount"],
        entity_rows=[
            {"customer_id":customer_id}
        ],
    )
    return response.to_dict()

if __name__ == "__main__":
    result = get_customer_features("5026.0")
    print(result)
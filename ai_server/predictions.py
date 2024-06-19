from db import get_dog_info_by_id
from model import get_labels

labels = get_labels()

def filtered_predictions(connection, predictions, threshold = 0.01):
    predictions = predictions[0].tolist()
    formated_predictions = [{"id": id, "score": float(score)} for id, score in enumerate(predictions)]
    filtered_predictions = [pred for pred in formated_predictions if pred["score"] >= threshold]
    # result 기본 snippet
    result = {"results_number" : len(filtered_predictions)} # 섞인 종 갯수
    # result에 각 prediction 아이템 추가 
    for prediction_item in filtered_predictions:
        dog_id = prediction_item["id"]+1
        # get a label
        label = labels[dog_id] if dog_id in labels else dog_id # 라벨을 한국어로 가져올 경우를 대비해서 쿼리 결과 말고 따로 csv 로 받아오는중
        # formatting score
        score = round(prediction_item["score"]* 100, 0)  # 계산을 위해 숫자 형식으로 남김 (float)
        # get information by dog_id
        dog_data = get_dog_info_by_id(connection, dog_id)
        size = dog_data[0][2]
        description = dog_data[0][3]
        info = dog_data[0][4]
        result[f"class_{dog_id}"] = [{"name" : label,
                                      "value" : score,
                                      "size": size,
                                      "description":description,
                                      "info":info}]
    return result
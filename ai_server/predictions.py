from model import get_labels

labels = get_labels()


def filtered_predictions(predictions, threshold = 0.01):
    predictions = predictions[0].tolist() 
    formated_predictions = [{"id": id, "score": float(score)} for id, score in enumerate(predictions)]
    filtered_predictions = [pred for pred in formated_predictions if pred["score"] >= threshold]

    # result 기본 snippet
    result = {"classification_number" : len(filtered_predictions), # 섞인 종 갯수
              "Information" : "양육정보를 추가해주세요!"} # 양육정보 

    # result에 rkr prediction 아이템 추가 
    for idx, prediction_item in enumerate(filtered_predictions):
        item_label = prediction_item["id"]+1
        label = labels[item_label] if item_label in labels else item_label
        score = round(prediction_item["score"], 2)
        result[f"classification_{idx+1:02}"] = [{"name" : label, "value" : score}] # 종 이름, 비율
    return result
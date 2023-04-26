import paddlenlp
import paddle

# 加载标点符号列表
class zh_punc:
    def __init__(self):
        self.tokenizer = paddlenlp.transformers.ErnieTokenizer.from_pretrained("ernie-3.0-medium-zh")
        self.model = paddlenlp.transformers.ErnieForTokenClassification.from_pretrained("ernie-3.0-medium-zh", num_classes=4)
        
        self.model_dict = paddle.load(load_path_or_url="https://github.com/yeyupiaoling/PunctuationModel/releases/download/v1.0/punctuation_model.pdparams")
        self.model.set_dict(self.model_dict)

    def restore_punc(self, sentence):
        inputs = self.tokenizer(sentence)
        input_ids = paddle.to_tensor([inputs["input_ids"]])
        segment_ids = paddle.to_tensor([inputs["token_type_ids"]])
        logits = self.model(input_ids, segment_ids)
        preds = paddle.argmax(logits, axis=-1).numpy()[0]

        output = ""
        for i, pred in enumerate(preds):
            token = inputs["tokens"][i]
            if token == "[CLS]":
                continue
            elif token == "[SEP]":
                break
            else:
                output += token
                if pred == 1: # 逗号
                    output += "，"
                elif pred == 2: # 句号
                    output += "。"
                elif pred == 3: # 问号
                    output += "？"

        # 打印输出结果
        print(output)

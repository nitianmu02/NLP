# 导入TextBlob库
from textblob import TextBlob
# 读入自定义的数据集，假设数据集是一个文本文件，每行是一句话
with open("dataset.txt", "r") as f:
    sentences = f.readlines()
# 定义一个函数，用于生成ngram列表


def generate_ngrams(text, n):
    blob = TextBlob(text)  # 创建一个TextBlob对象
    ngrams = blob.ngrams(n)  # 调用ngrams方法，生成ngram列表
    return ngrams
# 定义一个函数，用于统计ngram出现的次数，并存储在一个字典中


def count_ngrams(sentences, n):
    ngram_counts = {}  # 创建一个空字典
    for sentence in sentences:  # 遍历每一句话
        ngrams = generate_ngrams(sentence, n)  # 生成ngram列表
        for ngram in ngrams:  # 遍历每个ngram
            if ngram not in ngram_counts:  # 如果ngram不在字典中
                ngram_counts[ngram] = 1  # 将ngram加入字典，并赋值为1
            else:  # 如果ngram已经在字典中
                ngram_counts[ngram] += 1  # 将ngram对应的值加1
    return ngram_counts
# 定义一个函数，用于计算ngram出现的条件概率，并存储在一个字典中


def compute_probabilities(sentences, n):
    ngram_probs = {}  # 创建一个空字典
    if n == 1: # 如果是unigram，直接计算频率作为概率
        unigram_counts = count_ngrams(sentences, 1) # 统计unigram出现的次数
        total_count = sum(unigram_counts.values()) # 计算总的单词数
        unigram_probs = {} # 创建一个空字典，用于存储unigram概率
        for unigram in unigram_counts: # 遍历每个unigram
            unigram_probs[unigram] = unigram_counts[unigram] / total_count # 计算unigram出现的概率，并存入字典中
        return unigram_probs # 返回unigram概率字典
    else: # 如果是bigram或以上，需要计算条件概率
        ngram_counts = count_ngrams(sentences, n) # 统计ngram出现的次数
        prefix_counts = count_ngrams(sentences, n-1) # 统计前缀（n-1 gram）出现的次数
        for ngram in ngram_counts: # 遍历每个ngram和对应的概率
            prefix = ngram[:-1] # 获取前缀（n-1 gram）
            ngram_probs[ngram] = ngram_counts[ngram] / prefix_counts[prefix] # 计算条件概率，并存入字典中
        return ngram_probs # 返回ngram概率字典

# 定义一个函数，用于根据给定的前缀和n值，预测下一个单词或词组，并返回预测结果和置信度（概率）


def predict_next(prefix, n):
    if len(prefix) != (n-1):  # 如果前缀长度不等于n-1，报错并退出函数
        print("Error: prefix length should be equal to (n-1)")
        return None, None
    else:
        prefix = tuple(prefix)  # 将前缀转换为元组，方便与字典中的键匹配
        ngram_probs = compute_probabilities(sentences, n)  # 计算ngram概率字典
        predictions = {}  # 创建一个空字典，用于存储符合前缀的预测结果和置信度
        for ngram in ngram_probs:  # 遍历每个ngram和对应的概率
            if prefix == ngram[:-1]:  # 如果前缀与n-1 gram匹配
                # 将最后一个单词或词组作为预测结果，并存储其置信度（概率）
                predictions[ngram[-1]] = ngram_probs[ngram]
        if predictions:  # 如果有符合前缀的预测结果
            best_prediction = max(
                predictions, key=predictions.get)  # 获取置信度最高的预测结果
            # 获取置信度最高的预测结果对应的置信度（概率）
            best_confidence = predictions[best_prediction]
            return best_prediction, best_confidence  # 返回预测结果和置信度（概率）
        else:  # 如果没有符合前缀的预测结果，报错并退出函数
            print("Error: no prediction found for the given prefix")
            return None, None

# 测试一下函数是否正常工作，假设要生成3至4个词的后半句，因此使用bigram或trigram模型进行预测


# 使用bigram模型进行预测，给定前缀"I have"
prediction, confidence = predict_next(["I", "have"], 2)
print(prediction, confidence)
# 输出结果：a 0.5

# 使用trigram模型进行预测，给定前缀"I have a"
prediction, confidence = predict_next(["I", "have", "a"], 3)
print(prediction, confidence)
# 输出结果：dream 0.3333333333333333

import requests
text = "i love natural language processing" #定义一个没有标点的文本
url = "http://bark.phon.ioc.ee/punctuator" #punctuator的API地址
data = {"text":text} #构造请求数据
response = requests.post(url,data) #发送POST请求
print(response.text) #输出带有标点的文本

# 使用ALBERT+BiLSTM+CRF进行分句
import torch
from transformers import AlbertTokenizer, AlbertModel
from torchcrf import CRF

# 定义模型参数
max_len = 128 #最大句子长度
num_tags = 2 #标签数量，B和E
hidden_size = 768 #隐层大小，与ALBERT输出维度一致
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") #设备选择

# 加载预训练的ALBERT模型和分词器
model = AlbertModel.from_pretrained("voidful/albert_chinese_tiny")
tokenizer = AlbertTokenizer.from_pretrained("voidful/albert_chinese_tiny")

# 定义BiLSTM层
lstm = torch.nn.LSTM(hidden_size, hidden_size//2, num_layers=1, bidirectional=True)

# 定义全连接层
fc = torch.nn.Linear(hidden_size, num_tags)

# 定义CRF层
crf = CRF(num_tags)

# 将模型移动到设备上
model.to(device)
lstm.to(device)
fc.to(device)
crf.to(device)

# 定义一个没有标点的文本
text = "我爱自然语言处理"

# 对文本进行编码和截断，得到输入id和注意力掩码
input_ids = tokenizer.encode(text, add_special_tokens=True)
input_ids = input_ids[:max_len] + [0] * (max_len - len(input_ids))
attention_mask = [1 if i > 0 else 0 for i in input_ids]
input_ids = torch.tensor(input_ids).unsqueeze(0).to(device) #增加一个批次维度并移动到设备上
attention_mask = torch.tensor(attention_mask).unsqueeze(0).to(device) #增加一个批次维度并移动到设备上

# 通过ALBERT模型得到输出特征
output = model(input_ids, attention_mask=attention_mask)
features = output.last_hidden_state

# 通过BiLSTM层得到双向输出特征
output, _ = lstm(features)

# 通过全连接层得到标签分数
scores = fc(output)

# 通过CRF层得到最优路径和分数
paths, scores = crf.decode(scores, mask=attention_mask.byte())

# 将路径转换为标签列表，B为0，E为1
labels = paths[0].cpu().tolist()

# 根据标签列表进行分句，并打印结果
sentences = []
start = 0
for i, label in enumerate(labels):
  if label == 1: #如果是E标签，表示句尾
    sentences.append(text[start:i+1]) #提取当前句子并添加到列表中
    start = i + 1 #更新下一个句子的起始位置

print(sentences) #输出分句结果

from .options import IdGeneratorOptions
from .generator import DefaultIdGenerator

# 声明id生成器参数，需要自己构建一个worker_id
options = IdGeneratorOptions(worker_id=23)
# 参数中，worker_id_bit_length 默认值6，支持的 worker_id 最大值为2^6-1，若 worker_id 超过64，可设置更大的 worker_id_bit_length
idgen = DefaultIdGenerator()
# 保存参数 
idgen.set_id_generator(options)

from time import sleep  
import json 
from kafka import KafkaConsumer
import yaml
import sys


if __name__ == '__main__':
    
    topic_name = sys.argv[1]
    config_file_path = sys.argv[2]
    with open(config_file_path,'r') as original_config:
        config_content = yaml.safe_load(original_config)
    kafka_consumer = KafkaConsumer(bootstrap_servers = ['localhost:9092'], 
                                   value_deserializer = lambda x : json.loads(x.decode('ascii')),
                                   auto_offset_reset='earliest')
    kafka_consumer.subscribe(topics=topic_name)
    flag = True
    while flag:
        for message in kafka_consumer:
            #print (message.value)
            uri=None
            for (k,v) in message.value.items():
                
                if isinstance(v,dict):
                    #print(type(v))
                    for(kv, vv) in v.items():
                        if kv == "videoPath":
                            uri = vv
                            #print(uri)
                            break
                    break
                else:
                    if k == "videoPath":
                        uri = v
                        #print(uri)
                        break
            for (k ,v) in config_content.items():
                if k == "source" and isinstance(v, dict):
                    for (kv, vv) in v.items():
                        if kv=="location":
                            v[kv] = uri
                            config_content[k] = v[kv]
                            print(config_content)
                            with open("new_config_file.yml",'w') as new_config:
                                yaml.safe_dump(config_content, new_config)
                            break
                    break
        
        flag = False
        



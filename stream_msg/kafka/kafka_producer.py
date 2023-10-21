from time import sleep  
from json import dumps  
from kafka import KafkaProducer  
import sys


message = {
            "sensor" : {
    "id" : "HWY_20_AND_LOCUST__WBA__4_11_2018_4_59_59_379_AM_UTC-07_00",
    "type" : "Camera",
    "description" : "Aisle Camera",
    "location" : {
      "lat" : 45.293701446999997,
      "lon" : -75.830391449900006,
      "alt" : 48.155747933800001
    },
    "coordinate" : {
      "x" : 5.2000000000000002,
      "y" : 10.1,
      "z" : 11.199999999999999
    },
 
  "analyticsModule" : {
    "id" : "XYZ_2",
    "description" : "Vehicle Detection and License Plate Recognition 1",
    "source" : "OpenALR",
    "version" : "1.0"
  },
  "videoPath" : "file://opt/nvidia/deepstream/deepstream-6.1/samples/streams/sample_720p.mp4"
        }

}
message_simple = {
    "videoPath":"file://opt/nvidia/deepstream/deepstream-6.1/samples/streams/sample_720p.mp4"
}

message_minimal = {
        "command": "start-recording",
        "start": "2023-09-18T21:08:00.051Z",
        "end": "2023-09-18T21:10:02.851Z",
        "sensor": {
          "id": 0
        }
      }

if __name__ == "__main__":
    my_producer = KafkaProducer(  
        bootstrap_servers = ['localhost:9092'],  
        value_serializer = lambda x:dumps(x).encode('ascii')  
        )
    
    topic_name = sys.argv[1]
    times = int(sys.argv[2])
    print(topic_name + " : " + str(times))
    iterations = 0
    while iterations!=times:
        print(message_minimal)
        my_producer.send(topic_name, value=message_minimal) # topic name
        my_producer.flush()
        iterations +=1

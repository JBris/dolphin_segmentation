import pyarrow as pa

class Serializer:
    
    def serialize(self, data):
        return pa.serialize(data).to_buffer().to_pybytes()

    def deserialize(self, data):
        return pa.deserialize(data)
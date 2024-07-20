import pika, json

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        print(f"Put error: {err}", flush=True)
        return "Internal sever error", 500
    print(access, flush=True)
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"]
    }
    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        print(f"Publish channel error: {err}", flush=True)
        fs.delete(fid)                  
        return "Internal sever error", 500
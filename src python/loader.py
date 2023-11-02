import json,os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

json_formatter = JSONFormatter()

#based 5mins chunk
time_chunk_size_mins = 5

#extract subtitles using video_id 
def extract_subs(video_id : str) -> json:
    subs = YouTubeTranscriptApi.get_transcript(video_id)
    json_subs = json_formatter.format_transcript(transcript=subs)
    return json_subs

#save subs to sep direc
def save_subs(json_subs:str , print_dir : str , video_id : str):
   with open(f"{print_dir}/{video_id}.json" , mode= "w") as f:
       f.write(json_subs)

#create timebased chunk
def create_timechunk(input_dir :str , print_dir : str , time_chunk_size_mins):
    for filename in os.listdir(input_dir):
        file = os.path.join(input_dir,filename)
        f = open(file)
        data = json.loads(f.read())

        #creating empty dict which will add up
        timechunks = {}

        current_time_pos = 0

        #buffer refreshes after each time chunk created
        running_buffer = []
        chunk_num = 1

        #create time chunk
        for chunk in data:
            end_time = chunk["start"] + chunk["duration"]
            if end_time >= chunk_num * 60 * time_chunk_size_mins:           #endtime(seconds) >= 300 seconds approx for 1st iteration
                text = "".join(running_buffer)
                text = timechunks[current_time_pos - end_time]
                running_buffer.clear()
                current_time_pos = end_time
                chunk_num += 1
        running_buffer.append(chunk["text"])


        #!!!not processing last bit


        #updated to process last
        if running_buffer:
            text = "".join(running_buffer)
            timechunks[f"{current_time_pos} - {end_time}"] = text

        #saves the created chunk file
        with (f"{print_dir}/{filename}" , "w" ) as f:
            json.dump(timechunks,f)    








from pydub import AudioSegment
import subprocess
import soundfile as sf
import os

input_file1 = 'song1.mp3'
output_file_raw1 = 'song1.raw'
input_file2 = 'song2.mp3'
output_file_raw2 = 'song2.raw'
output_file_mp3 = 'mix.mp3'
end_file_mp3 = 'end.mp3'
final_file_mp3 = 'final.mp3'

#Change first mp3 file into raw file
command_raw1 = 'ffmpeg -i ' + input_file1 + ' -f s16le -acodec pcm_s16le ' + output_file_raw1
subprocess.run(command_raw1)

#Change second mp3 file into raw file
command_raw2 = 'ffmpeg -i ' + input_file2 + ' -f s16le -acodec pcm_s16le ' + output_file_raw2
subprocess.run(command_raw2)

#Read raw audio data of first file
audio_data1, sample_rate1 = sf.read(output_file_raw1, channels=1, samplerate=44100, subtype='PCM_16')

#Read raw audio data of second file
audio_data2, sample_rate2 = sf.read(output_file_raw2, channels=1, samplerate=44100, subtype='PCM_16')

#Makes sure files have the same frequency
assert sample_rate1 == sample_rate2

#Adjust to the min. length
min_length = min(len(audio_data1), len(audio_data2))
audio_data1_cropped = audio_data1[:min_length]
audio_data2_cropped = audio_data2[:min_length]

#Adds the audios
summed_audio_data = audio_data1_cropped + audio_data2_cropped

#If one song is longer than the other, the rest of the sound has to be added to the summed audio.
if(len(audio_data1)>len(audio_data2)):
    length=len(audio_data1)-min_length
    end=audio_data1[-length:]
elif(len(audio_data1)<len(audio_data2)):
    length=len(audio_data2)-min_length
    end=audio_data2[-length:]

#Save end audio into a raw file
end_file = 'final.raw'
sf.write(end_file, end, sample_rate1, subtype='PCM_16')

#Convert raw file into an mp3 file
command_mp3 = 'ffmpeg -f s16le -ar 44100 -ac 2 -i ' + end_file + ' ' + end_file_mp3
subprocess.run(command_mp3)

#Save summed audio into a raw file
output_file = 'audio_sumado.raw'
sf.write(output_file, summed_audio_data, sample_rate1, subtype='PCM_16')

#Convert raw file into an mp3 file
command_mp3 = 'ffmpeg -f s16le -ar 44100 -ac 2 -i ' + output_file + ' ' + output_file_mp3
subprocess.run(command_mp3)

#Add to the summed audio the end audio
song = AudioSegment.from_mp3(output_file_mp3) + AudioSegment.from_mp3(end_file_mp3)
song.export(final_file_mp3, format="mp3")


#Delete intermediate files

if os.path.isfile(output_file_mp3):
    os.remove(output_file_mp3)
else:
    # If it fails, inform the user.
    print("Error: %s file not found" % output_file_mp3)

if os.path.isfile(end_file_mp3):
    os.remove(end_file_mp3)
else:
    # If it fails, inform the user.
    print("Error: %s file not found" % end_file_mp3)

if os.path.isfile(output_file_raw1):
    os.remove(output_file_raw1)
else:
    # If it fails, inform the user.
    print("Error: %s file not found" % output_file_raw1)

if os.path.isfile(output_file_raw2):
    os.remove(output_file_raw2)
else:
    # If it fails, inform the user.
    print("Error: %s file not found" % output_file_raw2)

if os.path.isfile(end_file):
    os.remove(end_file)
else:
    # If it fails, inform the user.
    print("Error: %s file not found" % end_file)

if os.path.isfile(output_file):
    os.remove(output_file)
else:
    # If it fails, inform the user.
    print("Error: %s file not found" % output_file)
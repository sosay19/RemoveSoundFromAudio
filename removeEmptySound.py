from pydub import AudioSegment

def detect_moment_noise(sound, silence_threshold=-50.0, chunk_size=10):
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

def detect_moment_silence(sound, silence_threshold=-50.0, chunk_size=10):
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS > silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

original_sound = AudioSegment.from_file("./2020_07_13_12_53_02.wav", format="wav")

trim_moment_noise = detect_moment_noise(original_sound)
trim_moment_silence = detect_moment_silence(original_sound)

sound_without_silence = 0;
duration_original_sound = len(original_sound)    

if(trim_moment_noise !=0):
    original_sound = original_sound[trim_moment_noise:duration_original_sound]
else:
    sound_without_silence = original_sound[trim_moment_noise:trim_moment_silence]
    original_sound = original_sound[trim_moment_silence:duration_original_sound-trim_moment_silence]

while(trim_moment_noise != trim_moment_silence):
    trim_moment_noise = detect_moment_noise(original_sound)
    trim_moment_silence = detect_moment_silence(original_sound)
    if(trim_moment_noise !=0):
        original_sound = original_sound[trim_moment_noise:duration_original_sound]
    else:
        sound_without_silence += original_sound[trim_moment_noise:trim_moment_silence]
        original_sound = original_sound[trim_moment_silence:duration_original_sound-trim_moment_silence]

 
sound_without_silence.export("./sound_without_silence.wav", format="wav")
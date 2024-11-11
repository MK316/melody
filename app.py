import streamlit as st
from pydub import AudioSegment
from pydub.generators import Sine
import io

def note_to_tone(note_spec, base_duration=500):
    notes = {
        'do-1': 130.81, 're-1': 146.83, 'mi-1': 164.81, 'fa-1': 174.61, 'sol-1': 196.00,
        'la-1': 220.00, 'si-1': 246.94, 'do': 261.63, 're': 293.66, 'mi': 329.63,
        'fa': 349.23, 'sol': 392.00, 'la': 440.00, 'si': 493.88, 'do1': 523.25,
        're1': 587.33, 'mi1': 659.25, 'fa1': 698.46, 'sol1': 783.99, 'la1': 880.00,
        'si1': 987.77
    }
    parts = note_spec.split(':')
    note_part = parts[0]
    extra_commas = note_part.count(',')
    note_base = note_part.split(',')[0].lower()
    duration = int(parts[1]) if len(parts) > 1 else base_duration + 500 * extra_commas
    frequency = notes.get(note_base, 261.63)
    tone = Sine(frequency)
    audio = tone.to_audio_segment(duration=duration)
    return audio

def generate_melody(notes_input):
    melody = AudioSegment.silent(duration=0)
    for part in notes_input.split():
        tone = note_to_tone(part)
        melody += tone
    return melody

def play_sample_melody():
    sample_notes = "mi, sol-1 mi re do si-1 do fa, fa, fa, fa, mi, sol-1 mi re do si-1 do re, re, re, re,"
    return generate_melody(sample_notes)

# Streamlit interface
st.title('Create Your Melody')
sample_melody = play_sample_melody()
buffer = io.BytesIO()
sample_melody.export(buffer, format="wav")
buffer.seek(0)
st.audio(buffer, format='audio/wav')

user_input = st.text_input('Enter a sequence of notes (e.g., "do:1000, mi,, mi:750"): if you simply write "do re mi", the default duration is 500 ms. Using a comma doubles the duration.', '')
if st.button('Generate Tone'):
    user_melody = generate_melody(user_input)
    user_buffer = io.BytesIO()
    user_melody.export(user_buffer, format="wav")
    user_buffer.seek(0)
    st.audio(user_buffer, format='audio/wav')

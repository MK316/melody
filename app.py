import streamlit as st
from pydub import AudioSegment
from pydub.generators import Sine
import io

def note_to_tone(note_spec, base_duration=500):
    notes = {
        'do-1': 130.81, 'do#-1': 138.59, 're-1': 146.83, 're#-1': 155.56, 'mi-1': 164.81,
        'fa-1': 174.61, 'fa#-1': 184.99, 'sol-1': 196.00, 'sol#-1': 207.65, 'la-1': 220.00,
        'la#-1': 233.08, 'si-1': 246.94, 'do': 261.63, 'do#': 277.18, 're': 293.66,
        're#': 311.13, 'mi': 329.63, 'fa': 349.23, 'fa#': 369.99, 'sol': 392.00,
        'sol#': 415.30, 'la': 440.00, 'la#': 466.16, 'si': 493.88, 'do1': 523.25,
        'do#1': 554.37, 're1': 587.33, 're#1': 622.25, 'mi1': 659.25, 'fa1': 698.46,
        'fa#1': 739.99, 'sol1': 783.99, 'sol#1': 830.61, 'la1': 880.00, 'la#1': 932.33,
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
    sample_notes = "mi, sol-1 mi re do si-1 do fa, fa, fa, fa, mi, sol-1 mi re do si-1 do re, re, re, re#, mi, sol-1 mi re do si-1 do la, la, la, sol fa mi re sol-1 mi re, re, do,"
    return generate_melody(sample_notes)

# Streamlit interface
st.title('Create Your Melody')
st.caption("Sample melody: Salut d'amour, Op.12 (Elgar, Edward)")
st.caption("Input: mi, sol-1 mi re do si-1 do fa, fa, fa, fa, mi, sol-1 mi re do si-1 do re, re, re, re#, mi, sol-1 mi re do si-1 do la, la, la, sol fa mi re sol-1 mi re, re, do,")
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

# Display notes and instructions
table_markdown = """
| Symbol to use | Frequency (Hz) | Octave |
|---------------|----------------|--------|
| do-1          | 130.81         | C3     |
| do#-1         | 138.59         | C#3    |
| re-1          | 146.83         | D3     |
| re#-1         | 155.56         | D#3    |
| mi-1          | 164.81         | E3     |
| fa-1          | 174.61         | F3     |
| fa#-1         | 184.99         | F#3    |
| sol-1         | 196.00         | G3     |
| sol#-1        | 207.65         | G#3    |
| la-1          | 220.00         | A3     |
| la#-1         | 233.08         | A#3    |
| si-1          | 246.94         | B3     |
| do            | 261.63         | C4     |
| do#           | 277.18         | C#4    |
| re            | 293.66         | D4     |
| re#           | 311.13         | D#4    |
| mi            | 329.63         | E4     |
| fa            | 349.23         | F4     |
| fa#           | 369.99         | F#4    |
| sol           | 392.00         | G4     |
| sol#          | 415.30         | G#4    |
| la            | 440.00         | A4     |
| la#           | 466.16         | A#4    |
| si            | 493.88         | B4     |
| do1           | 523.25         | C5     |
| do#1          | 554.37         | C#5    |
| re1           | 587.33         | D5     |
| re#1          | 622.25         | D#5    |
| mi1           | 659.25         | E5     |
| fa1           | 698.46         | F5     |
| fa#1          | 739.99         | F#5    |
| sol1          | 783.99         | G5     |
| sol#1         | 830.61         | G#5    |
| la1           | 880.00         | A5     |
| la#1          | 932.33         | A#5    |
| si1           | 987.77         | B5     |
"""
st.markdown(table_markdown)

st.markdown(table_markdown)

import streamlit as st
from pydub import AudioSegment
from pydub.generators import Sine
import io

# Define a function to generate a tone for a note with complex duration specifications
def note_to_tone(note_spec, base_duration=500):
    notes = {
        'do-1': 130.81, 're-1': 146.83, 'mi-1': 164.81, 'fa-1': 174.61, 'sol-1': 196.00, 'la-1': 220.00, 'si-1': 246.94,
        'do': 261.63, 're': 293.66, 'mi': 329.63, 'fa': 349.23, 'sol': 392.00, 'la': 440.00, 'si': 493.88,
        'do1': 523.25, 're1': 587.33, 'mi1': 659.25, 'fa1': 698.46, 'sol1': 783.99, 'la1': 880.00, 'si1': 987.77
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
    sample_notes = "mi, sol-1 mi re do si-1 do fa, fa, fa, fa, re do1, si, la, sol, fa, mi, re, do,"
    return generate_melody(sample_notes)

# Streamlit interface
st.title('Create Your Melody')
st.caption('Sample to copy and paste: "mi, sol-1 mi re do si-1 do fa, fa, fa, fa, mi, sol-1 mi re do si-1 do re, re, re, re,"')
sample_melody = play_sample_melody()
st.audio(io.BytesIO(sample_melody.export(format="wav")), format='audio/wav')

user_input = st.text_input('Enter a sequence of notes (e.g., "do:1000, mi,, mi:750"): if you simply write "do re mi", the default duration is 500 ms. Using a comma doubles the duration.', '')
if st.button('Generate Tone'):
    user_melody = generate_melody(user_input)
    user_audio = io.BytesIO(user_melody.export(format="wav"))
    user_audio.seek(0)
    st.audio(user_audio, format='audio/wav')

# Display notes and instructions
table_markdown = """
| Symbol to use | Frequency (Hz) | Octave |
|------|----------------|--------|
| do-1 | 130.81         | C3     |
| re-1 | 146.83         | D3     |
| mi-1 | 164.81         | E3     |
| fa-1 | 174.61         | F3     |
| sol-1| 196.00         | G3     |
| la-1 | 220.00         | A3     |
| si-1 | 246.94         | B3     |
| do   | 261.63         | C4     |
| re   | 293.66         | D4     |
| mi   | 329.63         | E4     |
| fa   | 349.23         | F4     |
| sol  | 392.00         | G4     |
| la   | 440.00         | A4     |
| si   | 493.88         | B4     |
| do1  | 523.25         | C5     |
| re1  | 587.33         | D5     |
| mi1  | 659.25         | E5     |
| fa1  | 698.46         | F5     |
| sol1 | 783.99         | G5     |
| la1  | 880.00         | A5     |
| si1  | 987.77         | B5     |
"""
st.markdown(table_markdown)

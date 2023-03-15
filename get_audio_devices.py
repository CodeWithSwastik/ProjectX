# This file includes code subject to the MIT License. 
# For the full text of the license, see LICENSES/LICENSE-languageleapai.txt.
# The original code can be found at https://github.com/SociallyIneptWeeb/LanguageLeapAI.
# This modified code is also subject to the MIT License.

import speech_recognition as sr


if __name__ == '__main__':
    for mic_id, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        print(f'{mic_id}: {mic_name}')
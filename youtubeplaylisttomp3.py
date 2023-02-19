import pytube
import time
import os
import re
import moviepy.editor as mp


# SCRIPT FOR CONVERTING A YOUTUBE PLAYLIST TO MP3 LIST

playlist_input = input('Please input the link to the playlist you want to download and convert to mp3: ')
playlist = pytube.Playlist(playlist_input)
playlist_title = str(playlist.title)
save_folder = 'playlists'
playlist_folder = '{}/{}'.format(save_folder, playlist_title)
os_path = '{}\{}'.format(save_folder, playlist_title)

if not os.path.exists(os_path):
    os.mkdir(os_path)

print('\n Saving audio from the playlist {} in {}/{} ...'.format(playlist_title, save_folder,playlist_title))

ti = time.time()
print('---------------------------------------------------------------------------')
for i,video in enumerate(playlist.videos):
    if video.age_restricted:
        print('Skipping age restricted video: "{}"'.format(video.title))
        continue

    video.streams.filter(only_audio=True).first().download(playlist_folder)
    print('{} %'.format(int((i/len(playlist.videos))*100)))
print('100 %')

print('---------------------------------------------------------------------------')
print('Downloaded {} audio files from playlist: {} '.format(len(os.listdir(playlist_folder)), playlist_title))
print('Time taken: {:.0f} sec'.format(time.time() - ti))
print('---------------------------------------------------------------------------')

print('\n Converting {} mp4 files to mp3 ...'.format(len(os.listdir(playlist_folder))))

for file in os.listdir(os_path):
    if re.search('mp4',file):
        path_mp4 = os.path.join(os_path,file)
        path_mp3 = os.path.join(os_path, os.path.splitext(file)[0]+'.mp3')
        mp3_file = mp.AudioFileClip(path_mp4)
        mp3_file.write_audiofile(path_mp3)
        os.remove(path_mp4)

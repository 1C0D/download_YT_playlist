#from https://www.geeksforgeeks.org/download-youtube-videos-or-whole-playlist-with-python/
#I added a feature to clean filename titles and 
#another "fake button" on a same line, just to try it.

#pip install python-youtube
#pip install pytube

# Import Required Modules
from tkinter import *
from pyyoutube import Api, error
from pytube import YouTube
from threading import Thread
from tkinter import messagebox
  
  
def threading():
    # Call download_videos function
    t1 = Thread(target=download_videos)
    t1.start()
  
  
def download_videos():
    # Create API Object
    api = Api(api_key='Enter API Key')
  
    if "youtube" in playlistId.get():
        playlist_id = playlistId.get()[len(
            "https://www.youtube.com/playlist?list="):]
    else:
        playlist_id = playlistId.get()
  
    # Get list of video links
    try:
        playlist_item_by_id = api.get_playlist_items(
            playlist_id=playlist_id, count=0, return_json=True) #count=0 full playlist, json needed later in link
    except error.PyYouTubeException as e:
        messagebox.showinfo("error", e)
        return
        
    def clean(title):
        invalid = '<>:"/\|?* '
        invalid_0 = '\/|'  # -
        invalid_1 = '"<>:*?'  # '_' space

        for char in invalid:
            if char in title:
                if char in invalid_0:
                    title = title.replace(char, '-').strip()
                else:
                    title = title.replace(char, ' ').strip()
        title =' '.join(title.split())
        return title
  
    # Iterate through all video links
    for index, videoid in enumerate(playlist_item_by_id['items']):
          
        link = f"https://www.youtube.com/watch?v={videoid['contentDetails']['videoId']}"
  
        yt_obj = YouTube(link)
        
        #clean invalid char for filename (by default replaced by "" not good if you have ep1/2)
        title = yt_obj.title
        yt_obj.title = clean(yt_obj.title)
  
        filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')
  
        # download the highest quality video
        filters.get_highest_resolution().download()

        print(f"Downloaded:- {link} {title}")
  
    messagebox.showinfo("Success", "Video Successfully downloaded")
  
  
# Create Object
root = Tk()

#create frame for 2 buttons (just to do a try)
button_frame = Frame(root)
button_frame.pack(fill=X, side=BOTTOM)

# Set geometry
root.geometry('400x200')
  
# Add Label
Label(root, text="Youtube Playlist Downloader",
      font="italic 15 bold").pack(pady=10)
Label(root, text="Enter Playlist URL:-", font="italic 10").pack()
  
# Add Entry box
playlistId = Entry(root, width=60)
playlistId.pack(pady=20) #pady = space with previous item
  
# download_start = Button(root, text="Download Start", command=threading, anchor="w", width=30) anchor with width justify in the button
download_start = Button(button_frame, text="Download Start", command=threading)
download_start

#other button
run_button = Button(button_frame, text='fake button')
run_button

#to align fucking button
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

download_start.grid(row=0, column=0, pady=20)
run_button.grid(row=0, column=1)
  
# Execute Tkinter
root.mainloop()
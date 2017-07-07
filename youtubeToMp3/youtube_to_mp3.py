from __future__ import unicode_literals

import sys, getopt, os
import youtube_dl

class Audio:
    def __init__(self, argv):
        self.argv = argv
        self.links = None
        self.output = '%(title)s.%(ext)s'
        self.folder = os.path.join(os.getcwd(), 'Unknown')

    def __parse_arguments(self):
        try:
            opts, _ = getopt.getopt(self.argv,"hl:o:f:",
                                    ["link=","oname=","folder="])
        except getopt.GetoptError:
            self.__usage()
            return False
        for opt, arg in opts:
            if opt == '-h':
                self.__usage()
                return False
            elif opt in ('-l', "--link"):
                self.links = arg
            elif opt in ('-o', "--oname"):
                self.output = arg
            elif opt in ('-f', "--folder"):
                self.folder = os.path.join(os.getcwd(), arg)
                if not os.path.exists(self.folder):
                    os.makedirs(self.folder)
        if self.links == None:
            self.__usage()
            return False
        self.links = self.links.split(",")
        self.output = os.path.join(self.folder, self.output)
        return True

    def __usage(self):
        print('youtube_to_mp3.py -l <links separated via comma> [-o <output name>] [-f <folder>]')

    def download(self):
        self.__parse_arguments()
        options = {
            'format': 'bestaudio/best',
            'outtmpl': self.output,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with youtube_dl.YoutubeDL(options) as youtube:
            youtube.download(self.links)

if __name__ == "__main__":
    Audio(sys.argv[1:]).download()

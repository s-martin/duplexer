import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PDFHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory

    def on_modified(self, event):
        if not event.is_directory:
            self.check_pdfs()

    def check_pdfs(self):
        files = [f for f in os.listdir(self.directory) if f.endswith('.pdf')]
        if len(files) >= 2:
            even_pdf = os.path.join(self.directory, files[0])
            odd_pdf = os.path.join(self.directory, files[1])
            output_pdf = os.path.join(self.directory, 'collated.pdf')

            try:
                command = f"pdftk A={even_pdf} B={odd_pdf} shuffle A Bend-1 output {output_pdf}"
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                print(f"Collated PDF created: {output_pdf}")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e.output.decode('utf-8')}")

def watch_directory():
    directory = os.getenv('WATCH_DIRECTORY', '/app/uploads')
    event_handler = PDFHandler(directory)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    print(f"Watching directory: {directory}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_directory()

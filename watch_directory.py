import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PDFHandler(FileSystemEventHandler):
    def __init__(self, watch_directory, output_directory):
        self.watch_directory = watch_directory
        self.output_directory = output_directory

    def on_modified(self, event):
        if not event.is_directory:
            self.check_pdfs()

    def check_pdfs(self):
        files = [f for f in os.listdir(self.watch_directory) if f.endswith('.pdf')]
        if len(files) >= 2:
            even_pdf = os.path.join(self.watch_directory, files[0])
            odd_pdf = os.path.join(self.watch_directory, files[1])
            output_pdf = os.path.join(self.output_directory, 'collated.pdf')

            try:
                command = f"pdftk A={even_pdf} B={odd_pdf} shuffle A Bend-1 output {output_pdf}"
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                print(f"Collated PDF created: {output_pdf}")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e.output.decode('utf-8')}")

def watch_directory():
    watch_directory = os.getenv('WATCH_DIRECTORY', '/app/uploads')
    output_directory = os.getenv('OUTPUT_DIRECTORY', '/app/outputs')

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    event_handler = PDFHandler(watch_directory, output_directory)
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=False)
    observer.start()
    print(f"Watching directory: {watch_directory}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_directory()

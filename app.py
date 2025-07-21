from flask import Flask, request, jsonify, render_template, send_from_directory
import subprocess
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pdftk', methods=['POST'])
def pdftk():
    data = request.json
    command = data.get('command', '')
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return jsonify({'output': result.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.output.decode('utf-8')})

@app.route('/upload-and-collate', methods=['POST'])
def upload_and_collate():
    if 'even_pdf' not in request.files or 'odd_pdf' not in request.files:
        return jsonify({'error': 'No file part'}) 

    even_file = request.files['even_pdf']
    odd_file = request.files['odd_pdf']

    if even_file.filename == '' or odd_file.filename == '':
        return jsonify({'error': 'No selected file'})

    if even_file and odd_file:
        even_path = os.path.join(app.config['UPLOAD_FOLDER'], 'even.pdf')
        odd_path = os.path.join(app.config['UPLOAD_FOLDER'], 'odd.pdf')
        even_file.save(even_path)
        odd_file.save(odd_path) 

        output_pdf = os.path.join(app.config['OUTPUT_FOLDER'], 'collated.pdf')

        try:
            command = f"pdftk A={even_path} B={odd_path} shuffle A Bend-1 output {output_pdf}"
            subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return jsonify({'output_pdf': '/download/collated.pdf'})

        except subprocess.CalledProcessError as e:
            return jsonify({'error': e.output.decode('utf-8')})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

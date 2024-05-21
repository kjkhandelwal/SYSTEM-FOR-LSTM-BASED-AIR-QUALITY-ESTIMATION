from flask import Flask, jsonify
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

app = Flask(__name__)

@app.route('/api/run-ipython', methods=['GET'])
def run_ipython():
    ipynb_path = ipynb_path = os.path.join(os.path.dirname(__file__), 'app.py')
    
    # Load the IPython file
    with open(ipynb_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    # Run the IPython file
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': os.path.dirname(ipynb_path)}})
    
    # Get the output cells
    output_cells = [cell for cell in nb.cells if cell['cell_type'] == 'code' and 'outputs' in cell]
    
    # Extract the desired output (e.g., image and values)
    image_output = None
    values_output = None
    
    for cell in output_cells:
        for output in cell['outputs']:
            if 'data' in output and 'image/png' in output['data']:
                image_output = output['data']['image/png']
            elif 'data' in output and 'text/plain' in output['data']:
                values_output = output['data']['text/plain']
    
    # Return the output as JSON
    output = {
        'image': image_output,
        'values': values_output
    }
    
    return jsonify(output)

if __name__ == '__main__':
    app.run()

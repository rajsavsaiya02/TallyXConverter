# app/routes/api.py
import io
import pandas as pd
from flask import Blueprint, request, jsonify, Response
from ..utils.parser import parse_file_in_memory
from ..utils.xml_generator import generate_tally_xml

api_bp = Blueprint('api', __name__)


@api_bp.route('/preview-columns', methods=['POST'])
def preview_columns():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        filename = file.filename
        file_extension = filename.rsplit('.', 1)[1].lower()
        in_memory_buffer = io.BytesIO(file.read())

        # Performance: Read only the header row (nrows=0) to minimize memory and time.
        if file_extension == 'xlsx':
            df_header = pd.read_excel(in_memory_buffer, nrows=0)
        elif file_extension == 'csv':
            df_header = pd.read_csv(in_memory_buffer, nrows=0)
        else:
            raise ValueError("Unsupported file type")

        return jsonify({"columns": list(df_header.columns)}), 200

    except Exception as e:
        return jsonify({"error": f"Could not read file columns: {e}"}), 500


@api_bp.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    if 'mappings' not in request.form:
        return jsonify({"error": "Column mappings are required"}), 400

    file = request.files['file']
    # Mappings are sent as a JSON string from the frontend
    import json
    mappings = json.loads(request.form['mappings'])

    filename = file.filename
    in_memory_buffer = io.BytesIO(file.read())

    try:
        file_extension = filename.rsplit('.', 1)[1].lower()
        df = parse_file_in_memory(in_memory_buffer, file_extension, mappings)

        xml_data = generate_tally_xml(df)

        return Response(
            xml_data,
            mimetype='application/xml',
            headers={'Content-Disposition': 'attachment;filename=output.xml'}
        )

    except Exception as e:
        # Provide a specific, actionable error message.
        return jsonify({"error": f"Conversion failed: {e}"}), 500
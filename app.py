from flask import Flask, jsonify, request
from class_supportFunctions import SupportFunctions
from class_pytestGenerate import PytestGeneration

app = Flask(__name__)

def process_arguments(project,xmlPath,testcases,moshellcommand):
    pytestScript=PytestGeneration(project,xmlPath,testcases,moshellcommand)
    result=pytestScript.generate_pytest_script(moshellcommand,xmlPath,testcases,project)
    if result:
        return result
    else:
        return False

@app.route('/testbuild', methods=['POST'])
def api():

    supportFunction=SupportFunctions()

    # Check if the request contains JSON data
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Get JSON data from the request
    data = request.get_json()
    project = data.get('Project name')
    XMLpath = data.get('XMLPath must be a valid campaign XML with path')
    testcases = data.get('TestCases must be a list of test names')
    moshellcommand=data.get('Moshellcommand will be a string concatenated with ;')

    if type(project) != str:
        return jsonify({"error": "Invalid Project Name!"}), 400
    
    XMLpath_validation, XMLpath_result=supportFunction.is_valid_xml_file(XMLpath)
    if not XMLpath_validation:
        return jsonify({"error": XMLpath_result}), 400 

    listtype=supportFunction.check_list_type(testcases)
    if not (listtype=="List of numbers" or listtype=="List of strings"):
        return jsonify({"error": listtype}), 400 
    
    if type(moshellcommand) != str:
        return jsonify({"error": "Invalid Project Name!"}), 400

    # Call the Python function with the arguments
    result=process_arguments(project,XMLpath,testcases,moshellcommand)
    if result:
        return jsonify({'result': 'Pytest script generated successfully:'+result})
    else:
        return jsonify({"error": "No pytest script is generated"}), 400 
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)


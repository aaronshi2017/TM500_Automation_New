from flask import Flask, jsonify, request
from class_supportFunctions import SupportFunctions
from class_pytestGenerate import PytestGeneration
from class_gitHubhandling import class_gitHubUpload
from class_moshellWSL import class_moshellcommandWSL

app = Flask(__name__)

def process_arguments(project,xmlPath,testcases,moshellcommand):
    pytestScript=PytestGeneration(project,xmlPath,testcases,moshellcommand)
    result=pytestScript.generate_pytest_script()

    if result:
        github=class_gitHubUpload(project)
        github.github_upload()
        return result
    else:
        return False
    
@app.route('/moshell',methods=['POST'])
def moshell():
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Get JSON data from the request
    data = request.get_json()
    inputCommands = data.get('Moshell commands')
    default_command = 'moshell 169.254.2.2 "uv com_usernames=rbs;uv com_passwords=rbs;lt all;"'
    finalcommand = f"{default_command[:-1]}{inputCommands}\""
    print(finalcommand)
    moshell_obj=class_moshellcommandWSL()
    moshell_result=moshell_obj.execute_command(finalcommand)
    if moshell_result:
        return jsonify({'result': 'Moshell command execution\n:'+moshell_result})
    else:
        return jsonify({"error": "Something wrong"}), 400 
    

@app.route('/testbuild', methods=['POST'])
def api():

    supportFunction=SupportFunctions()

    # Check if the request contains JSON data
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Get JSON data from the request
    data = request.get_json()
    project = data.get('Project')
    XMLpath = data.get('XMLPath')
    testcases = data.get('TestCases')
    moshellcommand=data.get('Moshellcommand')

    if type(project) != str:
        return jsonify({"error": "Invalid Project Name!"}), 400
    
    WSLpath=supportFunction.windows_to_wsl_path(XMLpath)
    
    XMLpath_validation, XMLpath_result=supportFunction.is_valid_xml_file(WSLpath)
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


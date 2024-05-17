import os
from datetime import datetime
class PytestGeneration:
    def __init__(self,project,XMLpath,testcases,moshellcommand):
        self.project=project
        self.XMLpath=XMLpath
        self.testcases=testcases
        self.moshellcommand=moshellcommand

    def generate_pytest_script(moshellcommand, XMLpath, testcases, project):
        template="""
import pytest,time,re
from class_moshellWSL import class_moshellcommandWSL
from class_TMA_API import class_TMA_API

finalpath=""
finalverdict=""
sessionName=""

@pytest.fixture(scope="module")
def moshell_command():
    return class_moshellcommandWSL()

@pytest.fixture(scope="module")
def TMA_API():
    return class_TMA_API()

def test_step1_command(moshell_command):
    result=moshell_command.command_execution("{arg1}")
    print(result)
    assert result is not None

def test_step2_close_TMA(TMA_API):
    result1,result2=TMA_API.close_TMA()
    print(result1,result2)
    assert result1==200

def test_step3_open_TMA(TMA_API):
    result1,result2=TMA_API.open_TMA()
    print(result1,result2)
    assert result1==201

def test_step4_check_TMA_status(TMA_API):
    time.sleep(5)
    result1,result2=TMA_API.check_TMA_Status()
    print(result1,result2)
    assert result1==200

def test_step5_check_TMA_location(TMA_API):
    result1,result2=TMA_API.check_TMA_location()
    print(result1,result2)
    assert result1==200

def test_step6_schedule_campaign(TMA_API):
    path="{arg2}"
    testcase={arg3}
    result1,result2=TMA_API.schedule_campaign(path,testcase)
    print(result1,result2)
    assert result1==200

def test_step7_run_campaign_to_end(TMA_API):
    result1,result2=TMA_API.run_campaign_to_end()
    print(result1,result2)
    assert result1==202

def test_step8_generate_report_to_end(TMA_API):
    result1, result2 = TMA_API.generate_report_to_end()
    print(result1, result2)
    assert result1 == 200
    
    finalpath_match = re.search(r'C:\\\.*_session', result2)
    finalpath = finalpath_match.group()
    sessionName=finalpath.split("\\\\")[-1]
    assert finalpath_match is not None, "Final path not found"
    if finalpath is not None:
        print("The report folder is:",sessionName)
        assert sessionName is not None
    else:
        print("No report path found")

    finalverdict = result2[-4:]
    print("The final verdict is", finalverdict)
    assert finalverdict=="PASS"

def test_step9_update_report_to_database(TMA_API):
    if finalverdict=="PASS":
        result1, result2 = TMA_API.send_to_Database("{arg4}",sessionName,False)
        print(result1,result2)
        assert result1 == 200
    else:
        print(finalverdict)
        assert finalverdict is not None

    """
        script_content = template.format(
            arg1=moshellcommand,
            arg2=XMLpath,
            arg3=testcases,
            arg4=project
        )
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        testname='test_'+project+'_'+timestamp+'.py'
        try:
            with open(testname, 'w') as f:
                f.write(script_content)        
            print("Pytest script is created successfully.")
            return testname
        except:
            return False
    
    if __name__ == "__main__":
        # Example input values
        arg1 = "alt;st cell"
        arg2 = "C:\\Users\\rante\\Documents\\VIAVI\\TM500\\5G NR\\Test Mobile Application\\NLA7.4.3 Rev2\\MyCampaigns\\NPI_TC-01.xml"
        arg3 = ["1UE-Attach","1UE-UDP"]
        arg4 = 'TM500_Automaton_Auto_Generate1'
       
        generate_pytest_script(arg1, arg2, arg3, arg4)



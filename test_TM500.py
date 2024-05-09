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
    result=moshell_command.command_execution("alt;")
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
    # path="C:\\Users\\rante\\Documents\\VIAVI\\TM500\\5G NR\\Test Mobile Application\\NLA6.23.0 Rev5\\MyCampaigns\\5G-TestCases.xml"
    # path="C:\\Users\\rante\\Documents\\VIAVI\\TM500\\5G NR\\Test Mobile Application\\NLA7.4.3 Rev2\\MyCampaigns\\5G-TestCases_N7.xml"
    path="C:\\Users\\rante\\Documents\\VIAVI\\TM500\\5G NR\\Test Mobile Application\\NLA7.4.3 Rev2\\MyCampaigns\\NPI_TC-01.xml"
    testcase1=[0]
    testcase2=["1UE-Attach","1UE-UDP"]
    result1,result2=TMA_API.schedule_campaign(path,testcase1)
    print(result1,result2)
    assert result1==200

# def test_campaign_raw():
#     url_location="http://192.168.10.100:5099/rtc/v2/tmas/0001/campaigns/actions/schedule"
#     jsonData={
#     "FILE_PATH": "C:\\Users\\rante\\Documents\\VIAVI\\TM500\\5G NR\\Test Mobile Application\\NLA6.23.0 Rev5\\MyCampaigns\\5G-TestCases.xml",
#     "ITERATION_COUNT": 1,
#     "ACTION_ON_EVENT": 2,
#     "TESTS_SELECTION_BY_NAME": [
#         "1UE-Attach",
#         "1UE-UDP"
#     ]}
#     response = requests.post(url_location,data=json.dumps(jsonData),headers={"Content-Type": "application/json"})
#     print(response)
#     assert response.status_code==200

def test_step7_run_campaign_to_end(TMA_API):
    result1,result2=TMA_API.run_campaign_to_end()
    print(result1,result2)
    assert result1==202

# def test_run_MCI_command(TMA_API):
#     result1,result2=TMA_API.execute_MCI_command()
#     print(result1,result2)
#     assert result1==200

def test_step8_generate_report_to_end(TMA_API):
    # TMA_API=class_TMA_API()
    # TMA_API.scheduled="5G-TestCases_240506_071841646"
    result1, result2 = TMA_API.generate_report_to_end()
    print(result1, result2)
    assert result1 == 200
    
    finalpath_match = re.search(r'C:\\.*_session', result2)
    finalpath = finalpath_match.group()
    sessionName=finalpath.split("\\")[-1]
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
        result1, result2 = TMA_API.send_to_Database("NPI-Test-May-09",sessionName,False)
        print(result1,result2)
        assert result1 == 200
    else:
        print(finalverdict)
        assert finalverdict is not None

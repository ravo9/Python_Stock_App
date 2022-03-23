from pathlib import Path
import os


def checkIfTxtLogExists(outputDir):
    logFilePath = Path(outputDir + 'log.txt')
    if logFilePath.is_file() == False:
        os.system("mkdir " + outputDir)
        os.system("touch " + str(logFilePath))


def writeResultIntoTxtLog_set_name(outputDir, set_name = ""):
    checkIfTxtLogExists(outputDir)
    with open((outputDir + 'log.txt'),'a') as f:
        f.write("\n")
        f.write(set_name + "\n")


def writeResultIntoTxtLog_periods(outputDir, wholePeriodLength, subPeriodLength):
    checkIfTxtLogExists(outputDir)
    with open((outputDir + 'log.txt'),'a') as f:
        if (wholePeriodLength != None):
            f.write("WHOLE PERIOD LENGTH: " + wholePeriodLength + "\n")
        f.write("SUB-PERIOD LENGTH: " + str(subPeriodLength) + "\n")


def writeResultIntoTxtLog_results(outputDir, result, average_change):
    checkIfTxtLogExists(outputDir)
    with open((outputDir + 'log.txt'),'a') as f:
        f.write("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY IN PERCENTAGE: " + "{0:.2%}".format(result) + "\n")
        f.write("AVERAGE CHANGE OF GIVEN COMPANIES IN GIVEN PERIOD " + "{0:.2%}".format(average_change))
        f.write("\n\n")

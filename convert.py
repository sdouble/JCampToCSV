#! /usr/bin/env python
import datetime, re, sys
from itertools import islice

#True if running from gui, False if terminal
fromui=True

def countLinesInFile(file):
	return sum(1 for line in open(file))

def convert(ref, file_in, file_out):
	starttime = datetime.datetime.now()

	header=""
	spectraStart=None
	spectraStop=None
	spectraResolution=None
	spectraCount=0
	spectraTotal=None
	
	# RegEx patterns defined below
	header_origin = r"##ORIGIN=(.+)"
	header_blocks = r"##BLOCKS=([0-9]+)"
	header_owner = r"##OWNER="
	
	re_title = r"^##TITLE= (.+)"
	re_date = r"^##DATE=(.+)"
	re_time = r"^##TIME=(.+)"
	re_yfactor=r"##YFACTOR= (.+)"
	re_firstx = r"^##FIRSTX= (.+)"
	re_lastx = r"^##LASTX= (.+)"
	re_resolution = r"^##DELTAX= (.+)"
	re_xydata=r"^##XYDATA"
	re_end = r"^##END="
	re_npoints=r"##NPOINTS= ([0-9]+)"
	# RegEx patterns defined above
	
	newfile=open(file_out, "w")
	
	filename = file_in
	linecount=0
	totalLinesInfile=countLinesInFile(file_in)
	samplecount=0
	logging = False
	spectra=False
	result=header + "\n"
	
	with open(filename, "r") as in_file:
		for line in in_file:
			linecount+=1
			if fromui:
				ref.updateProgressBar(linecount,totalLinesInfile)
			m_owner=re.match(header_owner, line)
			m_sampleID = re.match(re_title, line)
			m_date = re.match(re_date, line)
			m_time = re.match(re_time, line)
			m_yfactor=re.match(re_yfactor, line)
			m_firstx=re.match(re_firstx, line)
			m_lastx=re.match(re_lastx, line)
			m_resolution=re.match(re_resolution, line)
			m_xydata=re.match(re_xydata, line)
			m_end=re.match(re_end, line)
			m_npoints=re.match(re_npoints, line)
	
			if m_owner:
				logging=True
			if m_sampleID:
				result+=m_sampleID.group(1)
			if m_date:
				result+="," + m_date.group(1)
			if m_time:
				result+="," + m_time.group(1)
			if m_yfactor:
				yfactor=m_yfactor.group(1)
			if m_firstx:
				spectraStart=m_firstx.group(1)
			if m_lastx:
				spectraStop=m_lastx.group(1)
			if m_resolution:
				spectraResolution=m_resolution.group(1)
			if m_xydata:
				spectra=True
			if m_npoints:
				spectraTotal=m_npoints.group(1)
			if m_end:
				samplecount+=1
				if fromui:
					ref.updateWinText("Samples: " + str(samplecount))
				if samplecount==1 and header and spectraResolution:
					newfile.write(header)
				newfile.write(result + "\n")
				result=""
				spectra=False
	
			if spectra and not m_xydata:
				line=line.lstrip()
				arr=line.split(' ')
				for entry in islice(arr, 1, None):
					if entry:
						spectraCount+=1
						if int(spectraCount) <= int(spectraTotal):
							result+="," + str(float(entry) * float(yfactor))
				if int(spectraCount) >= int(spectraTotal):
					spectraCount=0
	
			if spectraStart and spectraStop and spectraResolution and not header:
				header=",Date,Time"
				currentSpectra=float(spectraStart)
				while currentSpectra <= float(spectraStop):
					header+="," + str(currentSpectra)
					currentSpectra+=float(spectraResolution)
	
	newfile.close()
	print("Lines processed:", linecount)
	print("Samples extracted:", samplecount)
	print("Time elapsed:" , datetime.datetime.now() - starttime)

if __name__=="__main__":
	fromui=False
	if not len(sys.argv) == 3:
		print("\n Requires 2 parameters\n  arg1: source file (JCAMP-DX - *.dx)" +
			"\n  arg2: destination file (CSV output - *.csv)")
	else:
		convert(None, sys.argv[1], sys.argv[2])
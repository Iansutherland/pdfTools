#split a pdf into a page per file

import argparse #https://docs.python.org/2/howto/argparse.html
import os #https://docs.python.org/2/library/os.html
import re #https://docs.python.org/2/library/re.html
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger #https://pythonhosted.org/PyPDF2/

def split(outputDir, InputFilePath):
    inputFileName = os.path.dirname(InputFilePath)#Get the full path of the parent directory
    inputFileName = os.path.split(inputFileName)[1]#Get just the parent directories name (instead of the whole path)
    pdf = PdfFileReader(InputFilePath)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output = f'{outputDir}{inputFileName}{page}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

def merge(inputDir, outputFilePath):
    pdfMerger = PdfFileMerger()
    pdfList = findAllPdfFiles(inputDir)
    pdfList = sorted_nicely(pdfList)
    for path in pdfList:
        pdfMerger.append(PdfFileReader(path, 'rb'))
    pdfMerger.write(outputFilePath)

def findAllPdfFiles(inputDir):
    pdfList = []
    for file in os.listdir(inputDir):
        if file.endswith(".pdf"):
            pdfList.append(f'{inputDir}{file}')
    return pdfList

#https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

#returns a parser after setting up valid arguments
def parseCommandLine():
    parser = argparse.ArgumentParser(description="Split a pdf into individual pages OR merge multiple documents from a directory into one")
    exGroup = parser.add_mutually_exclusive_group(required=True)#user can only choose merge OR split
    exGroup.add_argument("-m", "--merge", help="specify merging, file will be created or overwritten", action="store_true")
    exGroup.add_argument("-s", "--split", help="specify splitting", action="store_true")
    parser.add_argument("file", type=str, help="Existing file for split, or desired merged file destination")
    parser.add_argument("directory", type=str, help="Existing dir full of pdfs for merging, or output dir for splitting")
    return parser


parser = parseCommandLine()
args = parser.parse_args()

userDirectoryExists = False
userFileExists = False

# print(args.file)
# print(args.directory)

if(os.path.isdir(args.directory)):
    userDirectoryExists = True

if(os.path.isfile(args.file)):
    userFileExists = True

if(args.merge == True and userDirectoryExists):
    merge(args.directory, args.file)
elif(args.split == True and userDirectoryExists and userFileExists):
    split(args.directory, args.file)
else:
    if(userDirectoryExists == False):
        raise IOError(5, "directory argument: {0} did not exist".format(args.directory))
    elif(userFileExists == False):
        raise IOError(5, "file argument: {0} did not exist".format(args.file))
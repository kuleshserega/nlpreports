# NLP Reports Analyzer

### How it works

* Util is read reports files (`*.txt`, you can change that using `REPORT_EXTENSION` configuration) from the folder which provides from the configuration.
* Marks the reports and move/copy (configurable `IS_COPY` option) them to the `OUTPUT_FOLDER`.
* Next, util is generating a script for `movescu` util for each folder that created for results.

### How reports are mark

* If `EXAM` section is absent in report-file then it's the report marks as the *UNKNOWN*.
* If `EXAM_KEYWORD` is absent in `EXAM` section, the report marks as the *NEGATIVE*.
* If `DESCRIPTION_KEYWORD` is absent bellow the `EXAM` section, the report marks as the *NEGATIVE*.
* In other scenarios, it's report marks as *POSITIVE*.

### Requirements

`Python >=3.6`

### Install

* Install from git: `pip install git+https://github.com/KirillLightIT/nlpreports`

* Install from local copy of this util: `python setup.py install`

### Usage

For the using this util you need to provide `config.env` file from the path that you running this util.
For generate template file of `config.env` you can run this util with the flag `--makeconfig`.

Also, you can provide all of the required variables with the command line.

Required variables:

```
folder, ip, port, aet, aec, aem, exam_keyword, description_keyword
```

#### Example of `config.env`  file

```
POSITIVE_BUCKET_NAME=Yes
NEGATIVE_BUCKET_NAME=No
UNKNOWN_BUCKET_NAME=Unknown
IP=127.0.0.1
PORT=104
AEM=Radflow
AEC=GATEWAY
AET=GATEWAY
IS_COPY=False
EXAM_KEYWORD=Chest
DESCRIPTION_KEYWORD=Pneumothorax
FOLDER=/data/reports
OUTPUT_FOLDER=/data/reports-result
REPORT_EXTENSION=txt
```

### Command line arguments

```
optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        Folder which need to analyze (Incoming). (default:
                        None)
  -o OUTPUT_FOLDER, --output OUTPUT_FOLDER
                        Folder where need to create and use the positive and
                        the negative folders. (By default create those folders
                        in the input folder)
  -c                    Just copy the reports, not move. (default: move)
  --ip IP               IP address for movescu util. (default: None)
  --port PORT           Port for movescu util. (default: None)
  --aet AET             Set my calling AE title. (default: None)
  --aec AEC             Set called AE title of peer. (default: None)
  --aem AEM             Set move destination AE title. (default: None)
  -e EXAM_KEYWORD, --exam-keyword EXAM_KEYWORD
                        Keyword which must be in EXAM section. (default: None)
  -d DESCRIPTION_KEYWORD, --description-keyword DESCRIPTION_KEYWORD
                        Keyword which must be in DESCRIPTION section.
                        (default: None)
  --makeconfig          Make config file in current directory.
```

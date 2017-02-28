

# O2 scraper

A simple web scraper to pull some phone billing data from O2's website. 

This was completed as a programming task as part of a recruitment process.

The scraper makes use of the Page Object Model in order to keep the design layout of the website kept separate from the scraper logic. This should make it easier to update the scraper *when* O2 update their website.

I've added a command line interface to enable the user to select the parameters to scrape. See the usage section before for examples of how this works.

## Installation
This project was built using Python 3.5

To install PhantomJS
~~~~
apt-get install node
apt-get install nodejs-legacy
apt-get install npm
npm -g install phantomjs
~~~~~

To install packages using pip

~~~~
pip3 install -r requirements.txt
~~~~

To install the o2scraper packages

~~~~
python3 setup.py install
~~~~

## Usage
In order to execute the script to fulfil the requirements of the spec, simply call scraper.py

~~~~
python3 scraper.py 
~~~~

There are a number of command line options to change the functionality of the script.

| 	|  	|                                                               	|
|----	|--------------	|--------------------------------------------------------------------------------------------	|
| -c 	| --countries  	| List of Countries to query                                         	|
| -t 	| --tariffType 	| The tariff types, one or more of 'pay_monthly' or 'pay_and go'). Defaults to 'pay_monthly' 	|
| -m 	| --methods    	| The communication method desired. One or more of 'landline', 'mobile', or 'text'           	|
|    	|              	|                                                                                            	|

Some examples:

~~~~
python3 scraper.py -c "Norway" -t pay_and_go -m mobile
~~~~

The above invocation will print the mobile charges for Noway on a pay and go contract
 
~~~~
python3 scraper.py -c "Canada" "Japan" "Guam" "Panama" -t pay_monthly pay_and_go -m landline text
~~~~ 

The above invocation will print the Landline and Text message charges for Canada, Japan, Guan and Panama for both Pay Monthly and Pay and Go contracts